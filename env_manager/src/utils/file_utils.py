
def read_file_to_string(file_path : str) -> str:
    """Reads the entire content of a file into a string."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def write_string_to_file(file_path : str, content : str):
    """Writes a given string to a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
