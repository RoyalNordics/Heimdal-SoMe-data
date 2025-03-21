#!/usr/bin/env python3
"""
Script to read all instruction files in the instructions folder and progress tracking files.
This script should be run each time Cline is started to load all instructions and current progress.
"""

import os
import sys
from pathlib import Path

def read_files_in_directory(directory, header):
    """
    Read all markdown files in the specified directory and print their content.
    
    Args:
        directory (Path): Path to the directory
        header (str): Header text to display before reading files
    """
    # Get all markdown files in the directory
    md_files = list(directory.glob("*.md"))
    
    if not md_files:
        print(f"No files found in '{directory}'.")
        return 0
    
    print(f"\n{'=' * 80}")
    print(f"{header} ({len(md_files)} file(s))")
    print(f"{'=' * 80}")
    
    # Read and print the content of each markdown file
    for md_file in md_files:
        print(f"\n{'=' * 80}")
        print(f"Reading from: {md_file.name}")
        print(f"{'=' * 80}\n")
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"Error reading file {md_file}: {e}")
    
    return len(md_files)

def read_instructions(instructions_dir="instructions", progress_dir="progress"):
    """
    Read all markdown files in the instructions and progress directories and print their content.
    
    Args:
        instructions_dir (str): Path to the instructions directory
        progress_dir (str): Path to the progress directory
    """
    # Get the absolute paths to the directories
    instructions_path = Path(instructions_dir).absolute()
    progress_path = Path(progress_dir).absolute()
    
    total_files = 0
    
    # Check if instructions directory exists
    if not instructions_path.exists() or not instructions_path.is_dir():
        print(f"Warning: Instructions directory '{instructions_path}' does not exist or is not a directory.")
    else:
        # Read instruction files
        files_count = read_files_in_directory(instructions_path, "INSTRUCTIONS")
        total_files += files_count
    
    # Check if progress directory exists
    if not progress_path.exists() or not progress_path.is_dir():
        print(f"Warning: Progress directory '{progress_path}' does not exist or is not a directory.")
    else:
        # Read progress files
        files_count = read_files_in_directory(progress_path, "CURRENT PROGRESS")
        total_files += files_count
    
    if total_files == 0:
        print("No instruction or progress files found.")
        sys.exit(0)
    
    print(f"\n{'=' * 80}")
    print(f"All instructions and progress information have been read. ({total_files} file(s) total)")
    print(f"{'=' * 80}\n")

if __name__ == "__main__":
    # If directories are provided as command-line arguments, use them
    if len(sys.argv) > 2:
        read_instructions(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        read_instructions(sys.argv[1])
    else:
        read_instructions()
