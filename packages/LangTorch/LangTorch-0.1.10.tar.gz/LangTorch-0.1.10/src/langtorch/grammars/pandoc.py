import pypandoc
import json

def convert_to_pandoc_ast(input_string: str, input_format: str) -> str:
    """
    Converts a given string into a Pandoc AST JSON format.

    Args:
        input_string (str): The input string to be converted.
        input_format (str): The format/language of the input string.

    Returns:
        str: A string containing Pandoc AST in JSON format.
    """
    try:
        # Convert the input string to Pandoc JSON format
        output = pypandoc.convert_text(input_string, 'json', format=input_format)
        return output
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Example Usage
ast_json = convert_to_pandoc_ast("Your input text here.", "markdown")
print(ast_json)
