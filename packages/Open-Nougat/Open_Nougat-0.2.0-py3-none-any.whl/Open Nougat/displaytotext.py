from IPython import display
import re

def displaytotext(file_path, remove_special=False):
    try:
        with open(file_path, 'r') as file:
            latex_content = file.read()
            
            if remove_special:
                latex_content = keep_only_text(latex_content)

            display.display(display.Latex(latex_content))
    except ImportError:
        def print_content(content):
            print(content)

        try:
            with open(file_path, 'r') as file:
                latex_content = file.read()

                if remove_special:
                    latex_content = keep_only_text(latex_content)

                print_content(latex_content)
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")

def keep_only_text(text):
    clean_pattern = re.compile(r'[^a-zA-Z\s]')
    clean_text = re.sub(clean_pattern, '', text)
    return clean_text