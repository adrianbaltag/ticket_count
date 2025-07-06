# pylint: disable=W0105
# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name, broad-except, too-many-locals, too-many-statements, too-many-branches, too-many-nested-blocks, too-many-boolean-expressions, too-many-arguments, consider-using-f-string
"""This module creates or updates a .txt file with NRB ticket details on the Desktop - my_tickets folder"""

import asyncio
import os
import re
from datetime import datetime

from colorama import Fore, init

from src.my_package.module1.extract_docx_info import (
    extract_investigation_info,
    find_nrb_docx,
)
from src.my_package.module1.nrb_ticket import get_nrb_ticket
from src.my_package.module1.read_docx import read_docx


async def create_or_update_ticket_file():
    """Create or update a .txt file with NRB ticket details on the Desktop - my_tickets folder"""
    init(autoreset=True)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    tickets_folder = os.path.join(desktop_path, "my_tickets")
    os.makedirs(tickets_folder, exist_ok=True)

    # Get NRB ticket file
    docx_file = await get_nrb_ticket()
    if not docx_file:
        print(Fore.RED + "No NRB .docx file found. Skipping file creation.")
        return

    # Extract ticket details
    ticket_number, phone_number, new_ticket_status = await read_docx(docx_file)

    # Validate ticket number
    if not ticket_number.strip():
        print(Fore.RED + "Invalid ticket number. Cannot create file.")
        return

    # Ensure ticket_number doesn't contain invalid filename characters
    ticket_number = re.sub(r'[\\/*?:"<>|]', "_", ticket_number.strip())
    ticket_number = ticket_number.replace("O", "0").replace(
        " ", ""
    )  # Replace 'o' with '0' for consistency

    # Ensure ticket status is only "wip" or "resolved"
    if new_ticket_status.lower() not in ["wip", "resolved"]:
        new_ticket_status = "wip"  # Default to "wip" if invalid

    # Check if a file with this ticket number exists
    existing_file_path = None
    for existing_file in os.listdir(tickets_folder):
        if existing_file.startswith(ticket_number) and existing_file.endswith(".txt"):
            existing_file_path = os.path.join(tickets_folder, existing_file)
            break

    # If a file exists, check the stored ticket status
    old_ticket_status = None
    if existing_file_path:
        try:
            with open(existing_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if "Ticket status:" in line:
                        status_text = line.strip().split(":", 1)[1].strip().lower()
                        # Extract only "wip" or "resolved"
                        status_match = re.search(r"\b(wip|resolved)\b", status_text)
                        old_ticket_status = (
                            status_match.group(1) if status_match else "wip"
                        )
                        break
        except Exception as e:
            print(Fore.RED + f"Error reading existing file: {e}")

        print(Fore.YELLOW + f"🔍 Found existing file: {existing_file_path}")
        print(Fore.YELLOW + f"🔍 Old status from file content: {old_ticket_status}")
        print(Fore.YELLOW + f"🔍 New extracted status: {new_ticket_status}")

        # Rename file if status changed
        if old_ticket_status and old_ticket_status != new_ticket_status:
            new_file_path = os.path.join(
                tickets_folder, f"{ticket_number}-{new_ticket_status.upper()}.txt"
            )
            try:
                os.rename(existing_file_path, new_file_path)
                print(
                    Fore.CYAN
                    + f"✅ Renamed file: {existing_file_path} → {new_file_path}"
                )
            except Exception as e:
                print(Fore.RED + f"Error renaming file: {e}")
            return  # Exit after renaming

    # Define new file path
    new_file_path = os.path.join(
        tickets_folder, f"{ticket_number}-{new_ticket_status.upper()}.txt"
    )

    try:
        # Create new ticket file
        with open(new_file_path, "w", encoding="utf-8") as file:
            file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"NRB Ticket: {ticket_number}\n")
            file.write(f"Phone Number: {phone_number}\n")
            file.write("------------------------------------\n")
            file.write(f"Ticket status: {new_ticket_status}\n")
            file.write("------------------------------------\n")

            # Extract investigation info if NRB file exists
            nrb_file = find_nrb_docx()
            if nrb_file:
                extracted_text = await extract_investigation_info(nrb_file)

                # Process extracted text
                paragraphs = [
                    p.strip() for p in extracted_text.split("\n") if p.strip()
                ]
                # Preserve order while removing duplicates
                unique_paragraphs = list(dict.fromkeys(paragraphs))

                # Remove the last paragraph if any exist
                if unique_paragraphs:
                    unique_paragraphs.pop()

                file.write("\n".join(unique_paragraphs) + "\n")
            else:
                print(Fore.YELLOW + "No NRB Word document found on the desktop.")

        print(Fore.GREEN + f"✅ File created: {new_file_path}")

    except Exception as e:
        print(Fore.RED + f"Error creating file {new_file_path}: {e}")


def rename_existing_files():
    """Scan existing .txt files in "my_tickets" and rename them if status inside has changed."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    tickets_folder = os.path.join(desktop_path, "my_tickets")

    if not os.path.exists(tickets_folder):
        print(Fore.RED + "The 'my_tickets' folder does not exist on the desktop.")
        return

    for file_name in os.listdir(tickets_folder):
        file_path = os.path.join(tickets_folder, file_name)

        if not file_name.endswith(".txt"):
            continue

        # Extract ticket number and status from filename
        match = re.match(r"^(NRB\d+)-(\w+)\.txt$", file_name, re.IGNORECASE)
        if not match:
            continue

        ticket_number, file_status = match.groups()
        file_status = file_status.lower()  # Normalize case

        try:
            # Read file content and identify lines
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            actual_status = None
            new_lines = []

            for line in lines:
                if line.startswith("Date:"):
                    new_date_line = (
                        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    new_lines.append(new_date_line)  # Update Date
                elif "Ticket status:" in line:
                    status_text = line.strip().split(":", 1)[1].strip().lower()
                    # Extract only "wip" or "resolved"
                    status_match = re.search(r"\b(wip|resolved)\b", status_text)
                    actual_status = status_match.group(1) if status_match else "wip"
                    new_lines.append(f"Ticket status: {actual_status}\n")
                else:
                    new_lines.append(line)

            # Debugging prints
            print(Fore.YELLOW + f"🔍 Checking file: {file_name}")
            print(Fore.YELLOW + f"🔍 Status from filename: {file_status}")
            print(Fore.YELLOW + f"🔍 Status inside file: {actual_status}")

            # Rename if status changed
            if actual_status and file_status != actual_status:
                new_file_name = f"{ticket_number}-{actual_status.upper()}.txt"
                new_file_path = os.path.join(tickets_folder, new_file_name)

                # Overwrite file with updated Date
                with open(file_path, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)

                os.rename(file_path, new_file_path)
                print(
                    Fore.CYAN
                    + f"✅ Renamed: {file_name} → {new_file_name} (Updated Date)"
                )

        except Exception as e:
            print(Fore.RED + f"Error processing {file_name}: {e}")


# Run the function if this script is executed directly
if __name__ == "__main__":
    asyncio.run(create_or_update_ticket_file())
    # Rename if status changed manually
    rename_existing_files()
