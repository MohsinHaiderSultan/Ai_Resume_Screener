import re
import string

def clean_text(text):
    """
    Cleans text by removing punctuation, extra whitespaces, and converting to lowercase.
    """
    if not text:
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove newlines and extra tabs
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()