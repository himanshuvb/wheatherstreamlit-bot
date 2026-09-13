"""
Configuration file for Campus Event Q&A Assistant.
Handles loading the system prompt from prompt.txt file.
"""

import os


def load_system_prompt() -> str:
    """Load the system prompt from prompt.txt file."""
    # TODO: Get the path to prompt.txt file
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompt.txt')
    
    # TODO: Open and read the prompt file
    with open(prompt_path, 'r') as f:
        prompt = f.read()
    
    # TODO: Return the content stripped of whitespace
    try:
        return prompt.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found at {prompt_path}. Please ensure prompt.txt exists.")    
    except Exception as e:
        raise Exception(f"An error occurred while loading the prompt: {str(e)}")
    # TODO: Handle FileNotFoundError with appropriate message

    # TODO: Handle other exceptions with appropriate message


def get_system_prompt() -> str:
    """Get the system prompt with user query placeholder."""
    # TODO: Call load_system_prompt() and return the result
    return load_system_prompt()


# TODO: Export the system prompt as SYSTEM_PROMPT
SYSTEM_PROMPT = get_system_prompt()
