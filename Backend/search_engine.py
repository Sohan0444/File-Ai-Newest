## Filters file index based on JSON criteria

from typing import List, Optional
from datetime import datetime, timedelta
from indexer import FileMetaData


def search_files(
    files: List[FileMetaData],
    name: Optional[str] = None,
    file_types: Optional[List[str]] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    before: Optional[datetime] = None,
    after: Optional[datetime] = None,
    sort_key: str = "name",
    reverse: bool = False,
    limit: Optional[int] = None
) -> List[FileMetaData]:
    # start with full index
    results = files  

    if name:
        results = _filter_by_name(results, name)

    if file_types:
        results = _filter_by_type(results, file_types)

    if min_size or max_size:
        results = _filter_by_size(results, min_size, max_size)

    if before or after:
        results = _filter_by_date(results, before=before, after=after)

    # always allow sorting
    results = sort_files(results, key=sort_key, reverse=reverse)

    if limit:
        results = _limit_results(results, limit)

    return results


def _filter_by_type(files: List[FileMetaData], file_types: List[str]) -> List[FileMetaData]:
    # keep only files whose type matches one of the requested extensions
    return [f for f in files if f.file_type in file_types]


def _filter_by_date(files: List[FileMetaData], before: datetime = None, after: datetime = None) -> List[FileMetaData]:
    filtered = []
    for f in files:
        # Convert string timestamps to datetime objects for comparison
        modified_dt = datetime.fromisoformat(f.modified) if isinstance(f.modified, str) else f.modified
        
        if before and modified_dt >= before:  # too new
            continue
        if after and modified_dt <= after:    # too old
            continue
        filtered.append(f)
    return filtered


def _filter_by_name(files: List[FileMetaData], keyword: str = None) -> List[FileMetaData]:
    if not keyword:
        return files  # no keyword → return everything
    filtered_files = []
    for f in files:
        if keyword.lower() in f.name.lower():  # case-insensitive match
            filtered_files.append(f)
    return filtered_files


def _filter_by_size(files: List[FileMetaData], min_size: int = None, max_size: int = None) -> List[FileMetaData]:
    filtered_files = []
    for f in files:
        if min_size is not None and f.size < min_size:  # too small
            continue
        if max_size is not None and f.size > max_size:  # too big
            continue
        filtered_files.append(f)
    return filtered_files


def sort_files(files: List[FileMetaData], key: str = "name", reverse: bool = False) -> List[FileMetaData]:
    key_map = {
        "name": lambda f: f.name,
        "size": lambda f: f.size,
        "modified": lambda f: datetime.fromisoformat(f.modified) if isinstance(f.modified, str) else f.modified,
        "accessed": lambda f: datetime.fromisoformat(f.accessed) if isinstance(f.accessed, str) else f.accessed
    }
    sort_key = key_map.get(key, key_map["name"])  # fallback to name
    return sorted(files, key=sort_key, reverse=reverse)


def _limit_results(files: List[FileMetaData], limit: int = None) -> List[FileMetaData]:
    if limit is None:
        return files
    return files[:limit]

#--------------------------------Test function--------------------------------
# Test function
def run_tests():
    # Create dummy files
    files = [
        FileMetaData(
            name="report1.pdf",
            path="/docs/report1.pdf",
            file_type="pdf",
            size=5000,
            created_at=datetime.now().isoformat(),
            modified=(datetime.now() - timedelta(days=2)).isoformat(),
            accessed=(datetime.now() - timedelta(days=1)).isoformat(),
            tags=[]
        ),
        FileMetaData(
            name="photo.jpg",
            path="/images/photo.jpg",
            file_type="jpg",
            size=2_000_000,
            created_at=datetime.now().isoformat(),
            modified=(datetime.now() - timedelta(days=10)).isoformat(),
            accessed=(datetime.now() - timedelta(days=5)).isoformat(),
            tags=[]
        ),
        FileMetaData(
            name="notes.txt",
            path="/docs/notes.txt",
            file_type="txt",
            size=200,
            created_at=datetime.now().isoformat(),
            modified=(datetime.now() - timedelta(days=1)).isoformat(),
            accessed=datetime.now().isoformat(),
            tags=[]
        ),
    ]

    print("=== PDFs only ===")
    results = search_files(files, file_types=["pdf"])
    for f in results:
        print(f.name, f.size)

    print("\n=== Files larger than 1MB ===")
    results = search_files(files, min_size=1_000_000)
    for f in results:
        print(f.name, f.size)

    print("\n=== Modified within last 3 days ===")
    results = search_files(files, after=datetime.now() - timedelta(days=3))
    for f in results:
        print(f.name, f.modified)

    print("\n=== Top 2 smallest files ===")
    results = search_files(files, sort_key="size", limit=2)
    for f in results:
        print(f.name, f.size)


if __name__ == "__main__":
    run_tests()







