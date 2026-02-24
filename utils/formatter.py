"""
Text Formatter Utilities
"""
import re


def escape_markdown(text: str, for_button: bool = False) -> str:
    """
    Escape special characters for MarkdownV2
    
    Args:
        text: Text to escape
        for_button: If True, use simpler escaping for button text
    
    Returns:
        Escaped text
    """
    if not text:
        return ""
    
    if for_button:
        # For buttons, only escape underscores that might cause issues
        return str(text)
    
    # MarkdownV2 special characters
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text


def create_progress_bar(completed: int, total: int, length: int = 6) -> str:
    """
    Create a progress bar
    
    Args:
        completed: Number of completed items
        total: Total number of items
        length: Length of the progress bar
    
    Returns:
        Progress bar string
    """
    if total == 0:
        return "▭" * length
    
    filled = int((completed / total) * length)
    empty = length - filled
    
    return "▬" * filled + "▭" * empty


def format_duration(seconds: int) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."
