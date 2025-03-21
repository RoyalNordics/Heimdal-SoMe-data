# Instructions Folder

This folder contains instructions that will be read each time Cline is started anew. 

## Purpose

- Store persistent instructions that should be loaded on startup
- Maintain a consistent set of guidelines and preferences
- Allow for easy updates to instructions over time

## Usage

Add markdown (.md) files to this folder with specific instructions. Each file should focus on a specific area or set of instructions.

Example files might include:
- `general_preferences.md` - General preferences and settings
- `coding_standards.md` - Coding standards and practices to follow
- `project_context.md` - Information about the current project
- `workflow.md` - Preferred workflow and processes

## Current Instructions

- `heimdal_data_collection.md` - Instructions for building a data collection module for Heimdal that fetches and stores data from social media, Google Trends, and SEO platforms.

When Cline starts, it should read all files in this folder to understand the user's preferences and requirements.
