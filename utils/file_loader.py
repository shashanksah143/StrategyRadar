def load_file_content(file_path: str) -> str:
    """
    Load file content from an absolute path and return as a string.
    
    Args:
        file_path: Absolute path to the file
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If the file cannot be read
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at {file_path}")
    except IOError as e:
        raise IOError(f"Unable to read file {file_path} - {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error reading file {file_path} - {str(e)}")