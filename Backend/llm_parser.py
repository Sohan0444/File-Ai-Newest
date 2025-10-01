##Sends prompt to llm/custom model
import json
import actions
 #Dummy function for now
def dummy_query(query: str) -> str:
    return "Find my last 5 pdfs"


##This function sends the query and all the tools avaible
def send_tools_openai(query: str):
    tools = [
    {
        "name": "find_files",
        "description": "Search for files by name, type, size, or date.",
        "parameters": {
            "type": "object",
            "properties": {
                "files" : {
                    "type": "array",
                    "items": {"type": "FileMetaData"},
                    "description" : "A list of filemetadata objects, filemetadata objects are simply a way to represent files in this project they have various properties like size, type, name, etc."
                },
                "name": {
                    "type": "string",
                    "description": "Part of the filename to search for"
                },
                "file_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file types (e.g., pdf, txt, jpg)"
                },
                "min_size": {
                    "type": "integer",
                    "description": "Minimum file size in bytes"
                },
                "max_size": {
                    "type": "integer",
                    "description": "Maximum file size in bytes"
                },
                "before": {
                    "type": "string",
                    "description": "Only include files modified before this date (ISO format: YYYY-MM-DD)"
                },
                "after": {
                    "type": "string",
                    "description": "Only include files modified after this date (ISO format: YYYY-MM-DD)"
                },
                "sort_key": {
                    "type": "string",
                    "description": "Field to sort by (default: 'name')"
                },
                "reverse": {
                    "type": "boolean",
                    "description": "Whether to sort in reverse order (default: false)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of files to return"
                }
            }
        }
    },
    {
        "name" : "get_file_info",
        "description" : "Get information about a file",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "file" : {"type" : "FileMetaData"}
            }
        }
    },
    {
        "name": "delete_file",
        "description": "Delete a file from the filesystem",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The absolute or relative path to the file to delete"
                }
            }
        }
    },
    {
        "name": "open_file",
        "description": "Open file with system default program",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to open"
                }
            }
        }
    },
    {
        "name": "move_file",
        "description": "Move file to a new location",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The current path of the file"
                },
                "destination": {
                    "type": "string",
                    "description": "The new location to move the file to"
                }
            }
        }
    },
    {
        "name": "copy_file",
        "description": "Copy file to a new location",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file to copy"
                },
                "destination": {
                    "type": "string",
                    "description": "The destination path for the copied file"
                }
            }
        }
    },
    {
        "name": "preview_file",
        "description": "Get a preview of file content (first N characters)",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to preview"
                },
                "chars": {
                    "type": "integer",
                    "description": "Number of characters to preview (default: 500)"
                }
            }
        }
    },
    {
        "name": "summarize_file",
        "description": "Use LLM to summarize file contents",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to summarize"
                }
            }
        }
    }
]

    return f"This is the user request {query}, \nThis is the list of tools available {tools}\nBased on the user request and the tools available, please return the appropriate tool and the parameters for the tool."


def interpret_tools_response(response: str):
    response = json.loads(response)
    return response['name'], response['parameters']


def call_tool(tool: str, parameters: dict):
    try:
        if tool == "find_files":
            result = actions.find_files(**parameters)
            return result
        elif tool == "get_file_info":
            return actions.get_file_info(parameters.get('file'))
        elif tool == "delete_file":
            return actions.delete_file(parameters.get('path'))
        elif tool == "open_file":
            return actions.open_file(parameters.get('path'))
        elif tool == "move_file":
            return actions.move_file(parameters.get('path'), parameters.get('destination'))
        elif tool == "copy_file":
            return actions.copy_file(parameters.get('path'), parameters.get('destination'))
        elif tool == "preview_file":
            return actions.preview_file(parameters.get('path'), parameters.get('chars', 500))
        elif tool == "summarize_file":
            return actions.summarize_file(parameters.get('path'))
        else:
            return f"Unknown tool: {tool}"
    except Exception as e:
        print(f"DEBUG: Exception occurred: {str(e)}")
        return f"Error calling {tool}: {str(e)}"
    

##TEST:
import os
from indexer import create_skeleton

# Create a fresh index from Downloads folder
downloads_path = os.path.expanduser("~/Downloads")
print(f"Indexing files from: {downloads_path}")

# Create index from Downloads folder
downloads_files = create_skeleton([downloads_path])
print(f"Found {len(downloads_files)} files in Downloads folder")

# Test finding PDFs from Downloads folder
fake_response = {
    "name": "find_files",
    "parameters": {
        "files": downloads_files,  # Use the Downloads files instead of default index
        "file_types": ["pdf"],
        "limit": 10,
        "sort_key": "modified",
        "reverse": True
    }
}
result = call_tool(fake_response["name"], fake_response["parameters"])
print(f"\nSearching for PDF files in Downloads: {len(result)} files found")

# Show details of the PDF files found
if result:
    print("\nPDF files found in Downloads:")
    for i, file in enumerate(result):
        print(f"  {i+1}. {file.name} - {file.size} bytes - Modified: {file.modified}")
else:
    print("No PDF files found in Downloads folder.")

# Let's see what file types are actually in Downloads
print("\n--- Checking what file types exist in Downloads ---")
all_downloads_files = call_tool("find_files", {"files": downloads_files, "limit": 20})
file_types = {}
for file in all_downloads_files:
    file_type = file.file_type if file.file_type else "no_extension"
    file_types[file_type] = file_types.get(file_type, 0) + 1

print("File types found in Downloads:")
for file_type, count in sorted(file_types.items()):
    print(f"  {file_type}: {count} files")

# Show some example files from Downloads
print(f"\nSample files from Downloads:")
for i, file in enumerate(all_downloads_files[:10]):
    print(f"  {i+1}. {file.name} ({file.file_type}) - {file.size} bytes")