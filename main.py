import asyncio

# import tracemalloc
import gc

# from datetime import datetime
from colorama import Fore, Style

from src.my_package.module1.count_tickets_status import count_ticket_status
from src.my_package.module1.delete_resolved_txt import clean_resolved_tickets
from src.my_package.module1.move_docx import move_docx
from src.my_package.module1.nrb_ticket import get_nrb_ticket
from src.my_package.module1.read_docx import read_docx
from src.my_package.module1.txt_file import (
    create_or_update_ticket_file,
    rename_existing_files,
)


def cleanup_memory():
    """Force garbage collection to free unused memory."""
    gc.collect()


async def main():
    """Main function to process NRB ticket files."""

    rename_existing_files()
    await clean_resolved_tickets()  # Cleanup before processing
    print(Style.DIM + "Starting new iteration")

    # Get the file name asynchronously
    file_name = await get_nrb_ticket()

    if file_name:
        # Extract information from the .docx file asynchronously
        nrb_ticket, phone_number, ticket_status = await read_docx(file_name)
        # Process and store ticket info
        await create_or_update_ticket_file()

        # Print and move the file
        print(Style.BRIGHT + f"Moving file: {file_name} to WORK_IN_PROGRESS folder")
        await move_docx(file_name)

        # Explicitly delete variables no longer needed to free memory
        del nrb_ticket
        del phone_number
        del ticket_status

    # Force garbage collection to clean up unused memory
    cleanup_memory()

    # Count ticket statuses
    await count_ticket_status()

    # # **Replace time.sleep with asyncio.sleep**
    await asyncio.sleep(3)

    # Force garbage collection to clean up after the status count
    cleanup_memory()


# Handle the KeyboardInterrupt gracefully
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{Fore.RED}Script interrupted by user.")
        print(f"{Fore.YELLOW}Exiting gracefully...")
        cleanup_memory()
