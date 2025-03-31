import asyncio
import os
import re

from colorama import Fore, Style, init
from docx import Document

from my_package.utils.decorators import remove_duplicates


def find_nrb_docx():
    """Search for a Word document on the desktop starting with 'NRB' and ending with '.docx'."""
    init(autoreset=True)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Search for a file matching the pattern "NRB*.docx"
    for file in os.listdir(desktop_path):
        if file.startswith("NRB") and file.endswith(".docx"):
            return os.path.join(desktop_path, file)  # Return first match

    return None  # No matching file found


@remove_duplicates
async def extract_investigation_info(file_path):
    """Extract investigation information from a Word document asynchronously."""
    if not file_path:
        print("No NRB file found on the desktop.")
        return ""

    print(Style.BRIGHT + f"Processing file: {file_path}")

    # Read the document asynchronously
    doc = await asyncio.to_thread(Document, file_path)

    investigation_info = []
    found_separator = False

    # Improved separator detection regex (matches only '=' lines)
    separator_pattern = r"^\s*=+\s*=*\s*$"

    # Iterate through paragraphs asynchronously
    for para in doc.paragraphs:
        clean_text = para.text.strip()  # Strip leading/trailing spaces

        if re.fullmatch(separator_pattern, clean_text):
            print(Style.BRIGHT + "Separator found! Collecting text now...")
            found_separator = True
            continue  # Skip the separator itself

        if found_separator and clean_text:  # Collect text after separator
            investigation_info.append(clean_text)

    # Join extracted text efficiently
    investigation_text = "\n".join(investigation_info).strip()

    if not investigation_text:
        print(Fore.RED + "No text found after separator!")
    else:
        print("Extracted Text:\n", investigation_text)

    return investigation_text


if __name__ == "__main__":
    # Example usage
    file_path = find_nrb_docx()
    asyncio.run(extract_investigation_info(file_path))
