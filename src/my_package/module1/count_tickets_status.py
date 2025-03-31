import asyncio
import os
import re

import aiofiles
from colorama import Back, Fore, init


async def count_ticket_status():
    """Counts the number of "wip" and "resolved" statuses from the "Ticket status:" line in .txt files in the "my_tickets" folder on the Desktop"""

    init(autoreset=True)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    my_tickets_folder = os.path.join(desktop_path, "my_tickets")

    if not os.path.exists(my_tickets_folder):
        print(Back.RED + "The 'my_tickets' folder does not exist on the desktop.")
        return

    wip_count = 0
    resolved_count = 0

    async def process_file(file_path):
        nonlocal wip_count, resolved_count
        try:
            async with aiofiles.open(file_path, "r", encoding="windows-1252") as file:
                async for line in file:
                    line_lower = line.strip().lower()

                    # Extract only the "Ticket status:" line
                    match = re.search(r"^ticket status:\s*(\w+)", line_lower)
                    if match:
                        status = match.group(1)
                        print(f"DEBUG - File: {file_path}, Found status: '{status}'")

                        if status == "wip":
                            wip_count += 1
                        elif status == "resolved":
                            resolved_count += 1
                        return  # Stop reading further lines after finding the status

        except Exception as e:
            print(Fore.RED + f"Error reading {file_path}: {e}")

    entries = await asyncio.to_thread(lambda: list(os.scandir(my_tickets_folder)))

    tasks = [
        process_file(entry.path)
        for entry in entries
        if entry.is_file() and entry.name.endswith(".txt")
    ]

    await asyncio.gather(*tasks)

    print(
        f"{Fore.YELLOW}WIP status: {Fore.LIGHTWHITE_EX}{wip_count}, {Fore.GREEN}Resolved status: {Fore.LIGHTWHITE_EX}{resolved_count}"
    )


if __name__ == "__main__":
    asyncio.run(count_ticket_status())
