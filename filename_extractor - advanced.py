import os
import sys
import traceback
from datetime import datetime

# Enable debug mode (set to False to disable debug output)
DEBUG = True

def debug_print(message, level="INFO"):
    """Print debug messages with timestamp"""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] [{level}] {message}")

def get_user_directory():
    """
    Ask user for directory path and validate it
    """
    debug_print("Requesting directory path from user")
    
    while True:
        print("\n" + "="*80)
        print("📂 DIRECTORY SELECTION")
        print("="*80)
        print("Enter the path of the directory you want to scan for files.")
        print("You can enter:")
        print("  - Full path (e.g., C:\\Users\\YourName\\Documents)")
        print("  - Relative path (e.g., ..\\..\\OtherFolder)")
        print("  - . (current directory)")
        print("  - Just press Enter to scan the same directory as this script")
        
        user_input = input("\n📁 Directory path: ").strip()
        
        # If user presses Enter, use script directory
        if not user_input:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            user_input = script_dir
            debug_print(f"User selected default (script directory): {user_input}")
            print(f"\n✓ Using script directory: {user_input}")
        
        # Expand user home directory if ~ is used
        if user_input.startswith('~'):
            user_input = os.path.expanduser(user_input)
            debug_print(f"Expanded home directory to: {user_input}")
        
        # Convert to absolute path
        try:
            absolute_path = os.path.abspath(user_input)
            debug_print(f"Absolute path: {absolute_path}")
        except Exception as e:
            debug_print(f"Error converting to absolute path: {e}", "ERROR")
            print(f"\n❌ Invalid path format: {user_input}")
            continue
        
        # Check if directory exists
        if not os.path.exists(absolute_path):
            debug_print(f"Directory does not exist: {absolute_path}", "ERROR")
            print(f"\n❌ Directory does not exist: {absolute_path}")
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry != 'y':
                debug_print("User chose to exit due to invalid directory")
                return None
            continue
        
        # Check if it's a directory
        if not os.path.isdir(absolute_path):
            debug_print(f"Path is not a directory: {absolute_path}", "ERROR")
            print(f"\n❌ Path is not a directory: {absolute_path}")
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry != 'y':
                debug_print("User chose to exit due to non-directory path")
                return None
            continue
        
        # Check read permissions
        if not os.access(absolute_path, os.R_OK):
            debug_print(f"No read permission for directory: {absolute_path}", "ERROR")
            print(f"\n❌ No read permission for directory: {absolute_path}")
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry != 'y':
                debug_print("User chose to exit due to permission denied")
                return None
            continue
        
        # Valid directory found
        debug_print(f"Valid directory selected: {absolute_path}")
        return absolute_path

def get_files_from_directory(directory_path):
    """
    Fetch all file names from the specified directory
    """
    debug_print(f"Starting to fetch files from: {directory_path}")
    
    files_list = []
    
    try:
        # Get all items in directory
        debug_print(f"Listing all items in directory...")
        all_items = os.listdir(directory_path)
        debug_print(f"Total items found (including directories): {len(all_items)}")
        
        # Count files vs directories
        file_count = 0
        dir_count = 0
        
        # Iterate through all items
        for idx, item in enumerate(all_items):
            debug_print(f"Processing item {idx+1}/{len(all_items)}: {item}")
            
            try:
                # Get the full path
                item_path = os.path.join(directory_path, item)
                debug_print(f"  Full path: {item_path}")
                
                # Check if it's a file
                if os.path.isfile(item_path):
                    file_count += 1
                    try:
                        file_size = os.path.getsize(item_path)
                        debug_print(f"  ✓ This is a file (size: {file_size} bytes)")
                    except:
                        debug_print(f"  ✓ This is a file (size: unable to determine)")
                    files_list.append(item)
                else:
                    dir_count += 1
                    debug_print(f"  ✗ This is a directory, skipping")
                    
            except Exception as e:
                debug_print(f"  Error processing item {item}: {e}", "ERROR")
                debug_print(f"  Traceback: {traceback.format_exc()}", "ERROR")
                continue
        
        debug_print(f"Scan complete - Files: {file_count}, Directories: {dir_count}")
        
    except PermissionError as e:
        debug_print(f"Permission denied accessing directory: {e}", "ERROR")
        debug_print(traceback.format_exc(), "ERROR")
        return []
    except OSError as e:
        debug_print(f"OS error accessing directory: {e}", "ERROR")
        debug_print(traceback.format_exc(), "ERROR")
        return []
    except Exception as e:
        debug_print(f"Unexpected error: {e}", "ERROR")
        debug_print(traceback.format_exc(), "ERROR")
        return []
    
    debug_print(f"Successfully collected {len(files_list)} file names")
    return files_list

def save_files_to_text(files_list, source_directory, output_filename="file_list.txt"):
    """Save the list of files to a text file in the script directory with UTF-8 encoding"""
    debug_print(f"Saving {len(files_list)} files to {output_filename}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)
    
    debug_print(f"Script directory (save location): {script_dir}")
    debug_print(f"Output path: {output_path}")
    
    try:
        # Try UTF-8 encoding first (supports all Unicode characters)
        debug_print("Attempting to save with UTF-8 encoding...")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("FILE LIST EXTRACTOR - USER DIRECTORY VERSION\n")
            f.write("="*80 + "\n")
            f.write(f"Source Directory Scanned: {source_directory}\n")
            f.write(f"Generated on: {datetime.now()}\n")
            f.write(f"Total files found: {len(files_list)}\n")
            f.write("="*80 + "\n\n")
            
            for idx, filename in enumerate(files_list, 1):
                try:
                    f.write(f"{idx:4d}. {filename}\n")
                except UnicodeEncodeError as e:
                    debug_print(f"  Unicode error on file {idx}: {filename[:50]}... - {e}", "WARNING")
                    # Try to write with error handling
                    f.write(f"{idx:4d}. {filename.encode('utf-8', 'ignore').decode('utf-8')}\n")
        
        debug_print(f"✓ File list saved successfully to: {output_path}")
        return output_path
        
    except Exception as e:
        debug_print(f"Error saving with UTF-8: {e}", "ERROR")
        
        # Fallback to ASCII with replacement
        try:
            debug_print("Attempting fallback with ASCII encoding (replacing non-ASCII)...")
            with open(output_path, 'w', encoding='ascii', errors='replace') as f:
                f.write("="*80 + "\n")
                f.write("FILE LIST EXTRACTOR - USER DIRECTORY VERSION\n")
                f.write("="*80 + "\n")
                f.write(f"Source Directory Scanned: {source_directory}\n")
                f.write(f"Generated on: {datetime.now()}\n")
                f.write(f"Total files found: {len(files_list)}\n")
                f.write("="*80 + "\n\n")
                
                for idx, filename in enumerate(files_list, 1):
                    f.write(f"{idx:4d}. {filename}\n")
                    
            debug_print(f"✓ File list saved with ASCII encoding to: {output_path}")
            return output_path
            
        except Exception as e2:
            debug_print(f"Error saving with fallback encoding: {e2}", "ERROR")
            debug_print(traceback.format_exc(), "ERROR")
            return None

def main():
    """Main function to run the script"""
    debug_print("="*60)
    debug_print("FILE NAME EXTRACTOR (USER DIRECTORY VERSION) STARTED")
    debug_print("="*60)
    
    # Get directory from user
    target_directory = get_user_directory()
    
    if not target_directory:
        debug_print("No valid directory selected, exiting", "ERROR")
        print("\n❌ No valid directory selected. Exiting...")
        return
    
    debug_print(f"Target directory confirmed: {target_directory}")
    
    # Get all files from the specified directory
    files = get_files_from_directory(target_directory)
    
    if not files:
        debug_print("No files found in the specified directory.", "ERROR")
        print(f"\n❌ No files found in: {target_directory}")
        print("Please check:")
        print("  1. The directory contains files (not just subdirectories)")
        print("  2. You have permission to read the files")
        return
    
    # Display results
    print(f"\n{'='*80}")
    print(f"📁 SCAN RESULTS:")
    print(f"{'='*80}")
    print(f"📍 Source Directory: {target_directory}")
    print(f"📊 Total files found: {len(files)}")
    print(f"{'='*80}\n")
    
    # Display first 20 files as preview
    preview_count = min(20, len(files))
    print(f"📋 Preview (first {preview_count} files):")
    for idx in range(preview_count):
        print(f"   {idx+1:4d}. {files[idx]}")
    
    if len(files) > preview_count:
        print(f"   ... and {len(files) - preview_count} more files")
    
    print(f"\n{'='*80}")
    
    # Auto-save to file in script directory
    debug_print("Auto-saving to file_list.txt in script directory...")
    saved_path = save_files_to_text(files, target_directory, "file_list.txt")
    
    if saved_path:
        print(f"\n✅ File list automatically saved to: {saved_path}")
        print(f"   (Saved in the same directory as this script)")
        debug_print("Auto-save completed successfully")
    else:
        print(f"\n❌ Failed to save file list automatically")
        debug_print("Auto-save failed", "ERROR")
    
    debug_print("="*60)
    debug_print("SCRIPT COMPLETED")
    debug_print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        debug_print("\nScript interrupted by user", "WARNING")
        print("\n\n⚠️  Script cancelled by user")
    except Exception as e:
        debug_print(f"Unexpected error in main: {e}", "ERROR")
        debug_print(traceback.format_exc(), "ERROR")
        print(f"\n❌ An unexpected error occurred: {e}")
        input("\nPress Enter to exit...")