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


def get_item_by_position(text_list: str, position: int) -> str:
    """
    Extract the Nth item from a numbered list (1-indexed).
    
    Args:
        text_list: Text containing numbered items (e.g., "1. biodata\n2. marriage biodata" or "1: biodata\n2: marriage biodata")
        position: Position to extract (1-indexed, e.g., 1 for first item)
        
    Returns:
        The cleaned item string without numbering, or None if position exceeds list length
        
    Example:
        >>> text = "1. biodata\\n2. marriage biodata"
        >>> get_item_by_position(text, 1)
        'biodata'
        >>> get_item_by_position(text, 2)
        'marriage biodata'
        
        # Works with URLs too:
        >>> urls = "1: https://example.com\\n2: https://test.com"
        >>> get_item_by_position(urls, 1)
        'https://example.com'
    """
    lines = [line.strip() for line in text_list.strip().split('\n') if line.strip()]
    if position <= len(lines):
        line = lines[position - 1]
        # Remove numbering: "1. biodata" -> "biodata" or "1: biodata" -> "biodata"
        if ': ' in line:
            return line.split(': ', 1)[1].strip()
        elif '. ' in line:
            return line.split('. ', 1)[1].strip()
        return line.strip()
    return None


# Backwards compatibility alias
def get_keyword_by_position(keywords_text: str, position: int) -> str:
    """
    Deprecated: Use get_item_by_position instead.
    Extract the Nth keyword from a numbered list (1-indexed).
    """
    return get_item_by_position(keywords_text, position)