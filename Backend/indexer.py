from pathlib import Path
from datetime import datetime
from unicodedata import name
import json
##Indexes files and metadata (data about data) to preform actions


# FileMetaData represents the metadata and attributes of a single file.
#
# Fields:
# - name: The name of the file (e.g. "resume.pdf")
# - path: Full absolute path to the file (e.g. "/Users/sohan/Documents/resume.pdf")
# - file_type: File extension/type without the dot (e.g. "pdf", "txt", "jpg")
# - size: File size in bytes (e.g. 324000 for ~324KB)
# - created_at: Timestamp of when the file was created
# - modified: Timestamp of last modification to the file
# - accessed: (Optional) Last time the file was accessed
# - folder: (Optional) Top-level folder name for quick grouping (e.g. "Downloads")
# - tags: (Optional) List of labels associated with the file (manual or AI-assigned)
# - preview_text: (Optional) Short content summary or snippet extracted from the file
# - hash: (Optional) SHA256 or similar hash of the file for duplicate detection
# - source: (Optional) Where the file came from — "local", "gdrive", "dropbox", etc.
# - owner: (Optional) Owner/creator of the file (useful in team/shared mode)
# - metadata: (Optional) Dictionary for storing any additional custom fields
class FileMetaData:
    def __init__(
        self,
        name,
        path,
        file_type,
        size,
        created_at,
        modified,
        accessed=None,
        folder=None,
        tags=None,
        preview_text=None,
        hash=None,
        source="local",
        owner=None,
        metadata=None,
    ):
        self.name = name
        self.path = path
        self.file_type = file_type
        self.size = size
        self.created_at = created_at
        self.modified = modified
        self.accessed = accessed
        self.folder = folder
        self.tags = tags or []
        self.preview_text = preview_text
        self.hash = hash
        self.source = source
        self.owner = owner
        self.metadata = metadata or {}  # Stores any extra metadata (if any)


##This function creates a skeleton of a users file system by returning a list of filemetadata.
def create_skeleton(root_paths: list) -> list[FileMetaData]:
    # This is the list that will store each file and its metadata
    file_index = []

    ##This loop recursively goes through each file and directory in the file system,
    # Path is an object that represents a file or directory path
    # .rgloc(*) means search every file and directory in the file system
    for r_p in root_paths:
        for path in Path(r_p).rglob("*"):
            if path.is_file():
                file_metadata = FileMetaData(
                    name=path.name,
                    path=str(path),  # Fixed: Use full path instead of just parent
                    file_type=path.suffix.lstrip("."),
                    size=path.stat().st_size,
                    created_at=datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
                    modified=datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                    accessed=datetime.fromtimestamp(path.stat().st_atime).isoformat(),
                    folder=path.parent.name,
                    tags=[],
                    preview_text=None,
                    hash=None,
                    source="local",
                    owner=None,
                    metadata={},
                )
                file_index.append((file_metadata))
    return file_index


# Re-scans the folders and:
# Adds any new files
# Updates changed files (e.g., modified date)
# Optionally removes deleted ones
# 🔁 This lets the app keep your index up to date without starting from scratch.
def refresh_index(existing_index: list[FileMetaData], root_paths: list) -> list[FileMetaData]:
    new_index = create_skeleton(root_paths)

    # Build a lookup dict from existing_index for fast access
    existing_lookup = {file.path: file for file in existing_index}

    for file in new_index:
        if file.path not in existing_lookup:
            existing_index.append(file)  # New file
        else:
            existing_file = existing_lookup[file.path]
            # Update fields that may have changed
            existing_file.modified = file.modified
            existing_file.accessed = file.accessed
            existing_file.size = file.size
            existing_file.tags = file.tags
            existing_file.preview_text = file.preview_text
            existing_file.hash = file.hash

    return existing_index



# Returns just a list of file names or paths from the index
# Helpful for quick lookups or debugging
def get_all_files(index: list[FileMetaData]) -> list[tuple[str, str]]:
    name_path_list = set()
    for files in index:
        name_path_list.add((files.name, files.path))
    return name_path_list


# Same idea — useful for folder-level organization/stats
def get_all_folders(index: list[FileMetaData]) -> list[str]:
    folder_list = []
    for files in index:
        folder_list.append(files.folder)
    return folder_list


# Returns a dictionary where keys are folder names and values are lists of files
# Super helpful when building UI later ("show me all files under X")
def group_by_folder(index: list[FileMetaData]) -> dict[str, list[FileMetaData]]:
    folder_dict = {}
    for files in index:
        if files.folder not in folder_dict:
            folder_dict.update({files.folder: [files]})
        else:
            folder_dict[files.folder].append(files)
    return folder_dict


# Save the index to a JSON file
def save_index(index: list[FileMetaData], file_path="file_index.json") -> None:
    """
    Saves a list of FileMetaData objects into a JSON file.
    Converts each FileMetaData into a dictionary before saving.
    """
    data = [vars(file) for file in index]  # Convert objects → dicts
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# Load the index from a JSON file
def load_index(file_path="file_index.json") -> list[FileMetaData]:
    """
    Loads a JSON file and converts dictionaries back into FileMetaData objects.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [FileMetaData(**file) for file in data]  # dicts → objects
    except FileNotFoundError:
        print(f"No index file found at {file_path}. Run create_skeleton() first.")
        return []







if __name__ == "__main__":
    index = create_skeleton([r"C:\Users\poiso\Desktop"])
    print(f"Total files found: {len(index)}\n")

    # Save it to a file
    save_index(index)

    # Load it later from the file
    loaded_index = load_index()
    print(f"Loaded {len(loaded_index)} files from cache")
    
    # Show first few files as examples
    for i, file in enumerate(index[:5]):  # Show first 5 files
        print(f"{i + 1}. {file.name} ({file.file_type}) — {file.path}")
    
    if len(index) > 5:
        print(f"... and {len(index) - 5} more files")