import asyncio
import datetime
import os


async def clean_resolved_tickets():
    """Cleans up resolved tickets from 'my_tickets' folder on Desktop if the ticket date is not today."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop, "my_tickets")

    if not os.path.exists(folder_path):
        print("Folder 'my_tickets' does not exist.")
        return

    today = datetime.date.today()

    async def process_file(file_name):
        file_path = os.path.join(folder_path, file_name)

        try:
            # Read file content in a separate thread
            content = await asyncio.to_thread(read_file, file_path)
            if not content:
                return  # Skip empty files or files that couldn't be read

            first_line, rest_of_file = content
            if first_line.startswith("Date:"):
                file_date_str = first_line.split("Date:")[1].strip().split()[0]
                file_date = datetime.datetime.strptime(file_date_str, "%Y-%m-%d").date()

                # Check for "resolved" and "wip" efficiently
                found_resolved = "resolved" in rest_of_file
                found_wip = "wip" in rest_of_file

                if found_resolved and not found_wip and file_date != today:
                    print(f"Deleting resolved ticket: {file_name}")
                    await asyncio.to_thread(os.remove, file_path)
                else:
                    print(f"Skipping: {file_name}")

        except (ValueError, IndexError, FileNotFoundError, OSError) as e:
            print(f"Error processing {file_name}: {e}")

    def read_file(file_path):
        """Helper function to read a file synchronously"""
        try:
            with open(file_path, "r", encoding="windows-1252") as file:
                first_line = file.readline().strip()  # Read first line
                rest_of_file = []  # Read the rest line by line to avoid memory issues
                for line in file:
                    rest_of_file.append(line.lower())

                # Return as a single string
                return first_line, " ".join(rest_of_file)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None  # Return None if file can't be read

    # Process all .txt files concurrently
    tasks = [process_file(f) for f in os.listdir(folder_path) if f.endswith(".txt")]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(clean_resolved_tickets())
