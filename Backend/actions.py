import os              # for file deletion, moving, copying
import shutil          # high-level file operations (move, copy)
import subprocess      # to open files with system default programs
from typing import List, Optional
from indexer import FileMetaData   # your custom file metadata class
import search_engine               # to call search_files
"""
actions.py

High-level actions a user (or LLM agent) can perform on files.
This wraps around indexer + search_engine and exposes 
"verbs" like find, delete, open, move, etc.
"""

from typing import List, Optional
from indexer import FileMetaData


def find_files(
    files: List[FileMetaData],
    name: Optional[str] = None,
    file_types: Optional[List[str]] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None,
    sort_key: str = "name",
    reverse: bool = False,
    limit: Optional[int] = None
) -> List[FileMetaData]:
    """
    Wrapper around search_engine.search_files.
    Takes filter parameters and returns matching files.
    """
    pass


def get_file_info(file: FileMetaData) -> dict:
   
    return {
        "name": file.name,            # filename only
        "path": file.path,            # full absolute path
        "size": file.size,            # file size in bytes
        "file_type": file.file_type,  # extension like pdf, txt, etc.
        "created": file.created,      # creation timestamp (datetime from indexer)
        "modified": file.modified,    # last modified timestamp
        "accessed": file.accessed,    # last accessed timestamp
        "tags": file.tags,            # custom tags if any
        "preview": file.preview_text  # short text snippet if available
    }



def delete_file(path: str) -> bool:
    """
    Deletes the file at given path.
    
    This function safely deletes a file from the filesystem with proper error handling.
    It performs several safety checks before attempting deletion to prevent data loss.
    
    Args:
        path (str): The absolute or relative path to the file to delete
        
    Returns:
        bool: True if deletion was successful, False if it failed
        
    Safety Features:
        - Checks if file exists before attempting deletion
        - Validates that the path points to a file (not a directory)
        - Handles permission errors gracefully
        - Provides detailed error logging for debugging
        
    Example:
        >>> delete_file("/path/to/file.txt")
        True
        >>> delete_file("/nonexistent/file.txt")
        False
    """
    try:
        # Step 1: Validate the input path
        if not path or not isinstance(path, str):
            print(f"Error: Invalid path provided: {path}")
            return False
            
        # Step 2: Convert relative path to absolute path for consistency
        # This ensures we're working with a full path regardless of input
        absolute_path = os.path.abspath(path)
        
        # Step 3: Check if the file actually exists
        # This prevents errors when trying to delete non-existent files
        if not os.path.exists(absolute_path):
            print(f"Error: File does not exist: {absolute_path}")
            return False
            
        # Step 4: Verify it's a file, not a directory
        # This prevents accidental deletion of entire folders
        if not os.path.isfile(absolute_path):
            print(f"Error: Path is not a file (might be a directory): {absolute_path}")
            return False
            
        # Step 5: Check if we have permission to delete the file
        # This catches permission errors before attempting deletion
        if not os.access(absolute_path, os.W_OK):
            print(f"Error: No write permission for file: {absolute_path}")
            return False
            
        # Step 6: Attempt to delete the file
        # os.remove() is the standard way to delete files in Python
        os.remove(absolute_path)
        
        # Step 7: Verify deletion was successful
        # Double-check that the file is actually gone
        if os.path.exists(absolute_path):
            print(f"Error: File still exists after deletion attempt: {absolute_path}")
            return False
            
        # Step 8: Success! Log the successful deletion
        print(f"Successfully deleted file: {absolute_path}")
        return True
        
    except PermissionError as e:
        # Handle permission-related errors (file in use, read-only, etc.)
        print(f"Permission error deleting file {path}: {e}")
        return False
        
    except OSError as e:
        # Handle other OS-related errors (disk full, network issues, etc.)
        print(f"OS error deleting file {path}: {e}")
        return False
        
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error deleting file {path}: {e}")
        return False
    


def open_file(path: str) -> bool:
    """
    Opens file with system default program.
    Returns True if successful, False otherwise.
    """
    pass


def move_file(path: str, destination: str) -> bool:
    """
    Moves file to a new location.
    Returns True if successful, False otherwise.
    """
    pass


def copy_file(path: str, destination: str) -> bool:
    """
    Copies file to a new location.
    Returns True if successful, False otherwise.
    """
    pass


def preview_file(path: str, chars: int = 500) -> str:
    """
    Returns first N characters of file content (if text-based).
    """
    pass


def summarize_file(path: str) -> str:
    """
    Uses LLM to summarize file contents.
    Stretch feature, requires LLM integration.
    """
    pass

