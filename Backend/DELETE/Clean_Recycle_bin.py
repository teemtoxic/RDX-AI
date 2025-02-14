import winshell
import logging

def clean_recycle_bin():
    """Clean the Windows Recycle Bin and return number of items removed."""
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        logging.info("Recycle bin cleaned successfully")
        return True
    except Exception as e:
        logging.error(f"Error cleaning recycle bin: {str(e)}")
        return False

if __name__ == "__main__":
    clean_recycle_bin()
