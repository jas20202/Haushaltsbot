import re
import uuid

def sanitize_string(input_string):
    """
    Sanitize a string to make it safe for SQL insertion.
    This should be used only in addition to parameterized queries.
    """
    # Entfernt SQL-Kommentare (--, /* */)
    sanitized = re.sub(r'(--|;|/\*|\*/)', '', input_string)
    
    # Escaping von einfachen und doppelten Anführungszeichen
    sanitized = sanitized.replace("'", "''").replace('"', '""')
    
    # Entfernt unnötige Leerzeichen am Anfang und Ende
    sanitized = sanitized.strip()
    
    # Entfernt Zeichen, die oft für SQL-Injections genutzt werden
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-_]', '', sanitized)
    
    return sanitized
