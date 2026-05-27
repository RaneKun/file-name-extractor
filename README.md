# 📁 File Name Extractor

![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

A Python utility that scans directories and exports all filenames to a formatted text file. Perfect for documenting file inventories, creating backup lists, or analyzing directory contents.

## ✨ Features

- **Two versions available:**
  - **Auto-scan mode** - Automatically scans the script's current directory (need to copy paste the script to the directory first)
  - **Interactive mode** - User specifies which directory to scan

- **Unicode Support** - Handles filenames in any language (Japanese, Arabic, Chinese, etc.)
- **Auto-save** - Automatically saves results to `file_list.txt` (same directory as that of the script)
- **Preview Mode** - Shows first 20 files in console
- **Debug Mode** - Optional detailed logging for troubleshooting
- **Error Handling** - Graceful handling of permissions and encoding issues

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## 🚀 Installation

1. Download the script you want to use:
   - `filename_extractor.py` - Auto-scan version
   - `filename_extractor_advanced.py` - Interactive version

2. Save the script to your desired location

3. Run with Python:
   ```bash
   python filename_extractor.py
   ```
   or
   ```bash
   python filename_extractor_advanced.py
