#!/usr/bin/env python3
"""
Comprehensive test suite for all tools in actions.py
Tests all the functions that can be called by the LLM parser
"""

import os
import sys
from datetime import datetime
from indexer import create_skeleton, FileMetaData
import actions

def print_separator(title):
    """Print a nice separator for test sections"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_find_files():
    """Test the find_files function with various parameters"""
    print_separator("TESTING FIND_FILES")
    
    # Get files from Downloads folder
    downloads_path = os.path.expanduser("~/Downloads")
    print(f"Indexing files from: {downloads_path}")
    downloads_files = create_skeleton([downloads_path])
    print(f"Found {len(downloads_files)} files in Downloads folder")
    
    # Test 1: Find all PDF files
    print("\n--- Test 1: Find all PDF files ---")
    pdf_files = actions.find_files(
        files=downloads_files,
        file_types=["pdf"],
        limit=5
    )
    print(f"Found {len(pdf_files)} PDF files:")
    for i, file in enumerate(pdf_files):
        print(f"  {i+1}. {file.name} - {file.size} bytes")
    
    # Test 2: Find files by name containing "resume"
    print("\n--- Test 2: Find files with 'resume' in name ---")
    resume_files = actions.find_files(
        files=downloads_files,
        name="resume",
        limit=5
    )
    print(f"Found {len(resume_files)} files with 'resume' in name:")
    for i, file in enumerate(resume_files):
        print(f"  {i+1}. {file.name} ({file.file_type}) - {file.size} bytes")
    
    # Test 3: Find large files (>100KB)
    print("\n--- Test 3: Find large files (>100KB) ---")
    large_files = actions.find_files(
        files=downloads_files,
        min_size=100000,
        limit=5
    )
    print(f"Found {len(large_files)} large files:")
    for i, file in enumerate(large_files):
        print(f"  {i+1}. {file.name} ({file.file_type}) - {file.size} bytes")
    
    # Test 4: Find files sorted by modification date
    print("\n--- Test 4: Find most recently modified files ---")
    recent_files = actions.find_files(
        files=downloads_files,
        sort_key="modified",
        reverse=True,
        limit=5
    )
    print(f"Found {len(recent_files)} most recent files:")
    for i, file in enumerate(recent_files):
        print(f"  {i+1}. {file.name} - Modified: {file.modified}")
    
    return downloads_files

def test_get_file_info(files):
    """Test the get_file_info function"""
    print_separator("TESTING GET_FILE_INFO")
    
    if not files:
        print("No files available to test get_file_info")
        return
    
    # Test with the first file
    test_file = files[0]
    print(f"Testing get_file_info with file: {test_file.name}")
    
    try:
        file_info = actions.get_file_info(test_file)
        print("File info retrieved successfully:")
        for key, value in file_info.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error getting file info: {e}")

def test_preview_file():
    """Test the preview_file function"""
    print_separator("TESTING PREVIEW_FILE")
    
    # Create a test text file
    test_file_path = "/tmp/test_preview.txt"
    test_content = "This is a test file for preview functionality.\nIt has multiple lines.\nLine 3: Testing preview with 50 characters limit."
    
    try:
        with open(test_file_path, "w") as f:
            f.write(test_content)
        
        print(f"Created test file: {test_file_path}")
        
        # Test preview with default character limit
        preview = actions.preview_file(test_file_path)
        print(f"Preview (default 500 chars): {preview}")
        
        # Test preview with custom character limit
        preview_short = actions.preview_file(test_file_path, chars=30)
        print(f"Preview (30 chars): {preview_short}")
        
        # Clean up
        os.remove(test_file_path)
        print("Test file cleaned up")
        
    except Exception as e:
        print(f"Error testing preview_file: {e}")

def test_copy_and_move_file():
    """Test copy_file and move_file functions"""
    print_separator("TESTING COPY_FILE AND MOVE_FILE")
    
    # Create a test file
    original_path = "/tmp/test_copy_original.txt"
    copy_path = "/tmp/test_copy_copy.txt"
    move_path = "/tmp/test_move_destination.txt"
    
    test_content = "This is a test file for copy and move operations."
    
    try:
        # Create original file
        with open(original_path, "w") as f:
            f.write(test_content)
        print(f"Created test file: {original_path}")
        
        # Test copy_file
        print("\n--- Testing copy_file ---")
        copy_result = actions.copy_file(original_path, copy_path)
        print(f"Copy result: {copy_result}")
        
        if os.path.exists(copy_path):
            print("✓ Copy successful - file exists at destination")
            with open(copy_path, "r") as f:
                copied_content = f.read()
            print(f"Copied content matches: {copied_content == test_content}")
        else:
            print("✗ Copy failed - file not found at destination")
        
        # Test move_file
        print("\n--- Testing move_file ---")
        move_result = actions.move_file(copy_path, move_path)
        print(f"Move result: {move_result}")
        
        if os.path.exists(move_path) and not os.path.exists(copy_path):
            print("✓ Move successful - file moved to new location")
        else:
            print("✗ Move failed")
        
        # Clean up
        for path in [original_path, copy_path, move_path]:
            if os.path.exists(path):
                os.remove(path)
        print("Test files cleaned up")
        
    except Exception as e:
        print(f"Error testing copy/move operations: {e}")

def test_delete_file():
    """Test the delete_file function"""
    print_separator("TESTING DELETE_FILE")
    
    # Create a test file to delete
    test_file_path = "/tmp/test_delete.txt"
    test_content = "This file will be deleted."
    
    try:
        # Create test file
        with open(test_file_path, "w") as f:
            f.write(test_content)
        print(f"Created test file: {test_file_path}")
        
        # Test delete_file
        delete_result = actions.delete_file(test_file_path)
        print(f"Delete result: {delete_result}")
        
        if not os.path.exists(test_file_path):
            print("✓ Delete successful - file no longer exists")
        else:
            print("✗ Delete failed - file still exists")
            
    except Exception as e:
        print(f"Error testing delete_file: {e}")
        # Clean up if file still exists
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_open_file():
    """Test the open_file function"""
    print_separator("TESTING OPEN_FILE")
    
    # Create a test file
    test_file_path = "/tmp/test_open.txt"
    test_content = "This is a test file for open operations."
    
    try:
        with open(test_file_path, "w") as f:
            f.write(test_content)
        print(f"Created test file: {test_file_path}")
        
        # Test open_file (this will actually try to open the file with system default)
        print("Testing open_file (will attempt to open with system default application)...")
        open_result = actions.open_file(test_file_path)
        print(f"Open result: {open_result}")
        
        # Clean up
        os.remove(test_file_path)
        print("Test file cleaned up")
        
    except Exception as e:
        print(f"Error testing open_file: {e}")

def test_summarize_file():
    """Test the summarize_file function"""
    print_separator("TESTING SUMMARIZE_FILE")
    
    # Create a test text file
    test_file_path = "/tmp/test_summarize.txt"
    test_content = """This is a test document for summarization.
    
It contains multiple paragraphs with various information.
The document discusses testing procedures and validation methods.
It includes details about file operations and system interactions.
The content is designed to test the summarization functionality.
"""
    
    try:
        with open(test_file_path, "w") as f:
            f.write(test_content)
        print(f"Created test file: {test_file_path}")
        
        # Test summarize_file
        print("Testing summarize_file...")
        summary = actions.summarize_file(test_file_path)
        print(f"Summary result: {summary}")
        
        # Clean up
        os.remove(test_file_path)
        print("Test file cleaned up")
        
    except Exception as e:
        print(f"Error testing summarize_file: {e}")

def main():
    """Run all tests"""
    print("Starting comprehensive tool testing...")
    print(f"Test started at: {datetime.now()}")
    
    try:
        # Test find_files and get some files for other tests
        files = test_find_files()
        
        # Test other functions
        test_get_file_info(files)
        test_preview_file()
        test_copy_and_move_file()
        test_delete_file()
        test_open_file()
        test_summarize_file()
        
        print_separator("ALL TESTS COMPLETED")
        print(f"Tests completed at: {datetime.now()}")
        print("✓ All tool functions have been tested")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
