### Universal Production Packer v.2.0
## Overview
This Python script is designed to pack production information (PI) and drawings for sections in a project. It creates organized directories for production information and drawings in a temporary location based on user input. The script utilizes Tkinter for the GUI and includes functionality to choose directories, pack information, and display results.

## How to Use
Select Sections: Click the "Select section directories" button to choose directories for the sections.

Specify Project Number: Enter the project number in the "Project number" entry.

Configure Production Folder Name: Optionally, you can change the default production folder name by modifying the "Production package title" entry.

Start Packaging: Click the "Start" button to initiate the packaging process.

## Results
The script will display the sections for which PI and drawings are successfully packed and indicate sections where PI is missing. The results will be shown in the corresponding text areas.

## Notes
Ensure the correct project number is entered.
Check for any warnings or errors in the process.
Clean outdated PI packages before starting a new packaging process.
## Requirements
Python 3
Tkinter, ttk, ThemedTk (installed via pip)
