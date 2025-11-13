import re
from typing import Optional, Tuple
def strip_markdown(text: str) -> str:
    """Remove common markdown syntax from text."""
    # Remove code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r"`.*?`", "", text)
    # Remove images ![alt](url)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    # Remove links [text](url)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Remove headings ###, ##, #
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    # Remove bold/italic *text*, **text**, _text_, __text__
    text = re.sub(r"(\*\*|__|\*|_)(.*?)\1", r"\2", text)
    return text

def extract_start_end(chunk_str: str) -> Optional[Tuple[int, int]]:
    """
    Nhận chuỗi kiểu "[start - end]" và trả về tuple (start, end).
    Trả về None nếu không tìm thấy pattern hợp lệ.
    """
    if not chunk_str:
        return None
    
    # Regex tìm [number - number]
    match = re.search(r"\[(\d+)\s*-\s*(\d+)\]", chunk_str)
    if match:
        start, end = int(match.group(1)), int(match.group(2))
        return start, end
    return None
