import re


def clean_lines_and_spaces(text,):
    text = text.replace("\n", " ")
    text = text.replace("\\n", " ")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")
    return text

def clean_text(text):
    """
    Sanitizes the input text by removing special characters (excluding spaces,
    digits, and alphabets),
    bullet points (•), and extra spaces. Periods are retained in the sanitized
    text.

    Parameters
    ----------
    text : str
        The text to be sanitized.

    Returns
    -------
    str
        The sanitized text without special characters and extra spaces,
        but with periods retained.

    Examples
    --------
    >>> text_to_sanitize = \"\"\"
    ...     Hello! This is a sample text with special characters: @#$%^&*(),
    ...     bullet points •, extra spaces, and new lines.
    ...
    ...     The text will be sanitized to remove all these elements.
    ... \"\"\"
    >>> sanitized_text = sanitize_text(text_to_sanitize)
    >>> print(sanitized_text)
    ...     Hello This is a sample text with special characters bullet points
    ...     extra spaces and new lines. The text will be sanitized to remove
    ...     all these elements.
    """
    text = re.sub(r'[^\w\s.]', '', text)
    text = clean_lines_and_spaces(text)
    text = text.replace('•', '')
    text = text.strip()
    return text
