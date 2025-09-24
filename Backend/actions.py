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
    Returns True if successful, False otherwise.
    """
    


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

