##Sends prompt to llm/custom model

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
                    "type": "FileMetaData",
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
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of files to return"
                }
            }
        }
    }
]

    return f"This is the user request {query}, "
