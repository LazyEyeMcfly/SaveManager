import os
import shutil
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox, Listbox, END, simpledialog

# Load saved paths for each game
CONFIG_FILE = "save_manager_config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        game_paths = json.load(f)
else:
    game_paths = {}

class SaveManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Save Manager V3")
        self.geometry("500x500")
        ctk.set_default_color_theme("dark-blue")  # Updated theme
        
        self.games = ["The Sims 4", "Skyrim", "Stardew Valley", "Fallout 4", "Baldur's Gate 3"]
        self.selected_game = ctk.StringVar(value=self.games[0])
        
        # UI Components
        self.create_widgets()
        self.load_game_paths()
    
    def create_widgets(self):
        ctk.CTkLabel(self, text="Select Game:").pack(pady=5)
        self.game_dropdown = ctk.CTkOptionMenu(self, values=self.games, variable=self.selected_game, command=self.switch_game)
        self.game_dropdown.pack(pady=5)
        
        ctk.CTkLabel(self, text="Save Folder:").pack(pady=5)
        self.save_folder_entry = ctk.CTkEntry(self, width=400)
        self.save_folder_entry.pack(pady=5)
        ctk.CTkButton(self, text="Browse", command=self.select_save_folder).pack(pady=5)
        
        ctk.CTkLabel(self, text="Backup Folder:").pack(pady=5)
        self.backup_folder_entry = ctk.CTkEntry(self, width=400)
        self.backup_folder_entry.pack(pady=5)
        ctk.CTkButton(self, text="Browse", command=self.select_backup_folder).pack(pady=5)
        
        ctk.CTkButton(self, text="Backup Saves", command=self.backup_saves).pack(pady=10)
        ctk.CTkButton(self, text="Restore Saves", command=self.restore_saves).pack(pady=10)
    
    def select_save_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_folder_entry.delete(0, END)
            self.save_folder_entry.insert(0, folder)
            self.update_game_paths()
    
    def select_backup_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.backup_folder_entry.delete(0, END)
            self.backup_folder_entry.insert(0, folder)
            self.update_game_paths()
    
    def update_game_paths(self):
        game = self.selected_game.get()
        game_paths[game] = {
            "save_folder": self.save_folder_entry.get(),
            "backup_folder": self.backup_folder_entry.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(game_paths, f, indent=4)
    
    def load_game_paths(self):
        game = self.selected_game.get()
        if game in game_paths:
            self.save_folder_entry.insert(0, game_paths[game].get("save_folder", ""))
            self.backup_folder_entry.insert(0, game_paths[game].get("backup_folder", ""))
    
    def switch_game(self, _):
        self.save_folder_entry.delete(0, END)
        self.backup_folder_entry.delete(0, END)
        self.load_game_paths()
    
    def backup_saves(self):
        save_folder = self.save_folder_entry.get()
        backup_folder = self.backup_folder_entry.get()
        if not save_folder or not backup_folder:
            messagebox.showerror("Error", "Please select valid folder paths before backing up.")
            return
        
        game_backup_folder = os.path.join(backup_folder, self.selected_game.get())
        os.makedirs(game_backup_folder, exist_ok=True)
        
        timestamp = self.get_timestamp()
        backup_path = os.path.join(game_backup_folder, timestamp)
        os.makedirs(backup_path)
        
        note = simpledialog.askstring("Backup Note", "Enter a note for this backup:")
        if note:
            with open(os.path.join(backup_path, "backup-note.txt"), "w") as f:
                f.write(note)
        
        for file in os.listdir(save_folder):
            shutil.copy(os.path.join(save_folder, file), backup_path)
        
        messagebox.showinfo("Success", "Backup completed successfully!")
    
    def restore_saves(self):
        backup_folder = self.backup_folder_entry.get()
        if not backup_folder:
            messagebox.showerror("Error", "Please select a valid backup folder.")
            return
        
        game_backup_folder = os.path.join(backup_folder, self.selected_game.get())
        if not os.path.exists(game_backup_folder):
            messagebox.showerror("Error", "No backups found!")
            return
        
        restore_window = ctk.CTkToplevel(self)
        restore_window.title("Select a Backup to Restore")
        restore_window.geometry("400x400")
        
        backup_listbox = Listbox(restore_window, height=10)
        backup_listbox.pack(pady=10, padx=10, fill="both", expand=True)
        
        backups = sorted(os.listdir(game_backup_folder), reverse=True)
        for backup in backups:
            note_path = os.path.join(game_backup_folder, backup, "backup-note.txt")
            note_text = ""
            if os.path.exists(note_path):
                with open(note_path, "r") as f:
                    note_text = f.read().strip()
            backup_listbox.insert(END, f"{backup} - {note_text}")
        
        def restore_selected():
            selected_index = backup_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a backup to restore.")
                return
            
            selected_backup = backups[selected_index[0]]
            restore_path = os.path.join(game_backup_folder, selected_backup)
            
            save_folder = self.save_folder_entry.get()
            for file in os.listdir(restore_path):
                if file != "backup-note.txt":
                    shutil.copy(os.path.join(restore_path, file), save_folder)
            
            messagebox.showinfo("Success", "Backup restored successfully!")
            restore_window.destroy()
        
        ctk.CTkButton(restore_window, text="Restore Selected", command=restore_selected).pack(pady=10)
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
if __name__ == "__main__":
    app = SaveManagerApp()
    app.mainloop()
