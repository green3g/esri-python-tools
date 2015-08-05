#a collection of string functions

def get_safe_string(text):
    """returns a safe string that can be used for file names"""
    return "".join([c for c in text if c.isalnum()]).rstrip()