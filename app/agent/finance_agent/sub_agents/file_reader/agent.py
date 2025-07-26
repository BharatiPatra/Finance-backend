import os
from google import genai
from google.genai import types
import pathlib
from dotenv import load_dotenv
import pdfplumber

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def file_reader_tool() -> str:
    """
    Read the uploaded pdf file and return its content.
    Args:
        None

    Returns:
        str: The content of the pdf file.
    """
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent
    file_path = BASE_DIR / "data" / "pdf" / "file.pdf"
    if not file_path.exists():
        return "There is no file uploaded."
    page_texts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=True)
            if text:
                # `text` already contains its own '\n' breaks
                page_texts.append(text)
    # Join pages with a blank line (or just '\n') between them
    return "\n\n".join(page_texts)


if __name__ == "__main__":
    answer = file_reader_tool()
    print(answer)
