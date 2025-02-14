import os
import shutil
import logging
from pathlib import Path

def clear_temp_files():
    """Clear temporary files from Windows system."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Common temp directories
    temp_locations = [
        os.environ.get('TEMP'),
        os.environ.get('TMP'),
        os.path.join(os.environ.get('WINDIR'), 'Temp')
    ]
    
    files_removed = 0
    
    for temp_dir in temp_locations:
        if not temp_dir or not os.path.exists(temp_dir):
            continue
            
        try:
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    files_removed += 1
                    logging.info(f"Removed: {item_path}")
                except Exception as e:
                    logging.error(f"Error removing {item_path}: {str(e)}")
                    
        except Exception as e:
            logging.error(f"Error accessing {temp_dir}: {str(e)}")
    
    return files_removed

if __name__ == "__main__":
    removed = clear_temp_files()
    print(f"Successfully removed {removed} temporary items")
