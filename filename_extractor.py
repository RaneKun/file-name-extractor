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

def get_all_files_in_script_folder():
    """
    Fetch all file names from the folder containing this script
    """
    debug_print("Starting to fetch files from script directory")
    
    # Get the directory where the script is located
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        debug_print(f"Script directory: {script_dir}")
    except Exception as e:
        debug_print(f"Error getting script directory: {e}", "ERROR")
        debug_print(traceback.format_exc(), "ERROR")
        return []
    
    # Check if directory exists
    if not os.path.exists(script_dir):
        debug_print(f"Script directory does not exist: {script_dir}", "ERROR")
        return []
    
    debug_print(f"Directory exists, checking permissions...")
    
    # Check if readable
    if not os.access(script_dir, os.R_OK):
        debug_print(f"No read permission for directory: {script_dir}", "ERROR")
        return []
    
    files_list = []
    
    try:
        # Get all items in directory
        debug_print(f"Listing all items in directory...")
        all_items = os.listdir(script_dir)
        debug_print(f"Total items found (including directories): {len(all_items)}")
        
        # Count files vs directories
        file_count = 0
        dir_count = 0
        
        # Iterate through all items
        for idx, item in enumerate(all_items):
            debug_print(f"Processing item {idx+1}/{len(all_items)}: {item}")
            
            try:
                # Get the full path
                item_path = os.path.join(script_dir, item)
                debug_print(f"  Full path: {item_path}")
                
                # Check if it's a file
                if os.path.isfile(item_path):
                    file_count += 1
                    debug_print(f"  ✓ This is a file (size: {os.path.getsize(item_path)} bytes)")
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

def save_files_to_text_auto(files_list, output_filename="file_list.txt"):
    """Automatically save the list of files to a text file with UTF-8 encoding"""
    debug_print(f"Automatically saving {len(files_list)} files to {output_filename}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)
    
    debug_print(f"Output path: {output_path}")
    
    try:
        # Try UTF-8 encoding first (supports all Unicode characters)
        debug_print("Attempting to save with UTF-8 encoding...")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("FILE LIST EXTRACTOR - AUTO GENERATED\n")
            f.write("="*80 + "\n")
            f.write(f"Source Directory: {script_dir}\n")
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
                f.write("FILE LIST EXTRACTOR - AUTO GENERATED\n")
                f.write("="*80 + "\n")
                f.write(f"Source Directory: {script_dir}\n")
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
    debug_print("FILE NAME EXTRACTOR (AUTO-SAVE VERSION) STARTED")
    debug_print("="*60)
    
    # Get all files
    files = get_all_files_in_script_folder()
    
    if not files:
        debug_print("No files found or unable to access directory.", "ERROR")
        print("\n❌ No files found or unable to access directory.")
        print("Please check:")
        print("  1. The script has permission to read the directory")
        print("  2. There are actually files in this directory")
        print("  3. The script is in the correct location")
        return
    
    # Display results
    print(f"\n{'='*80}")
    print(f"📁 FILES IN SCRIPT DIRECTORY:")
    print(f"{'='*80}")
    print(f"📍 Location: {os.path.dirname(os.path.abspath(__file__))}")
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
    
    # Auto-save to file
    debug_print("Auto-saving to file_list.txt...")
    saved_path = save_files_to_text_auto(files, "file_list.txt")
    
    if saved_path:
        print(f"\n✅ File list automatically saved to: {saved_path}")
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