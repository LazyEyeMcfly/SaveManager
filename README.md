Overview

Save Manager V3 is a modern, multi-game save file backup and restoration tool. Built with customtkinter, it provides a sleek, user-friendly interface to manage game saves efficiently.
Features:

    Select from a list of supported games.
    Define and store custom save and backup folder locations.
    Create timestamped backups with optional notes.
    Restore backups from a list of saved versions.
    Maintain multiple game profiles with persistent configurations.

Supported Games

    The Sims 4
    Skyrim
    Stardew Valley
    Fallout 4
    Baldur's Gate 3

Users can manually add support for additional games by specifying their save and backup directories.
Installation
Requirements:

    Python 3.8+
    Install dependencies:

    pip install customtkinter

Running the Application:

python save_manager_v3.py

Usage Guide

    Select a game from the dropdown menu.
    Set save & backup folders using the browse buttons.
    Click "Backup Saves" to create a timestamped backup.
    Click "Restore Saves", select a backup, and confirm restoration.

Configuration

The application stores game paths in save_manager_config.json, preserving save and backup folder settings between sessions.
Future Enhancements

    Auto-detect save directories for supported games.
    Implement versioning control for backups.
    Expand support for additional games with predefined save locations.

License

This project is open-source and free to use. Contributions and feedback are welcome!
