# Heimdal-SoMe-data

## Instructions and Progress Tracking System

This repository contains a system for storing and loading instructions for Cline, as well as tracking the progress of the project. The instructions are stored in the `instructions` folder, and the progress is tracked in the `progress` folder. Both can be read using the provided scripts.

### Structure

- `instructions/` - Folder containing all instruction files
  - `README.md` - Explains the purpose and usage of the instructions folder
  - `heimdal_data_collection.md` - Instructions for building a data collection module for Heimdal
- `progress/` - Folder containing progress tracking files
  - `current_status.md` - Tracks the current status of the project, including completed tasks, current tasks, and next steps
- `read_instructions.py` - Python script to read all instruction and progress files
- `start_cline.sh` - Shell script to start Cline and load all instructions and progress information

### Usage

To start Cline with all instructions and progress information loaded, run:

```bash
./start_cline.sh
```

This will:
1. Read all instruction files in the `instructions` folder
2. Read all progress tracking files in the `progress` folder
3. Display their content
4. Start Cline with all instructions and progress information loaded

### Adding New Instructions

To add new instructions:

1. Create a new markdown (.md) file in the `instructions` folder
2. Add your instructions to the file
3. Update the `instructions/README.md` file to include your new instruction file

The next time you run `./start_cline.sh`, your new instructions will be loaded.

### Updating Progress

To update the progress of the project:

1. Edit the `progress/current_status.md` file
2. Update the "Last Updated" section with the current date and time
3. Update the "Current Status", "Completed Tasks", "Current Tasks", and "Next Steps" sections as needed
4. Add any new issues or challenges to the "Issues/Challenges" section
5. Add any additional notes to the "Notes" section

The next time you run `./start_cline.sh`, the updated progress information will be loaded.
