import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


def save_output_file(content: str, file_format: str = "txt", filename: Optional[str] = None) -> dict:
    """
    Save content to the output folder with today's date (dd/mm/yyyy structure).
    Creates the dated folder if it doesn't exist.
    
    Args:
        content: The content to save (as string)
        file_format: File format - "json" or "txt" (default: "txt")
        filename: Optional filename without extension. If not provided, uses timestamp.
        
    Returns:
        Dictionary with:
            - success: True if file saved successfully, False otherwise
            - file_path: Full path to the saved file if success is True
            - error: Error message if success is False
    """
    try:
        # Get today's date in dd-mm-yyyy format
        today = datetime.now()
        date_folder = today.strftime("%d-%m-%Y")
        
        # Construct the output directory path
        output_dir = Path(__file__).parent.parent / "output" / date_folder
        
        # Create the directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = today.strftime("%H-%M-%S")
            filename = f"output_{timestamp}"
        
        # Remove extension from filename if present
        filename = filename.split('.')[0]
        
        # Determine file extension and process content
        if file_format.lower() == "json":
            file_extension = ".json"
            # If content is a string but should be JSON, try to parse it
            try:
                if isinstance(content, str):
                    content_to_write = json.dumps(json.loads(content), indent=2)
                else:
                    content_to_write = json.dumps(content, indent=2)
            except json.JSONDecodeError:
                # If it's not valid JSON, save as is
                content_to_write = content
        else:  # txt or any other format defaults to txt
            file_extension = ".txt"
            content_to_write = content
        
        # Construct full file path
        file_path = output_dir / f"{filename}{file_extension}"
        
        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_to_write)
        
        return {
            "success": True,
            "file_path": str(file_path)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to save file - {str(e)}"
        }
