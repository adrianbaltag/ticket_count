
# Ticket_Count

This script does the following: copy paragraphs form a word doc into a .txt file, keep count of TOTAL "wip" | "resolved" tickets.
For a indepth  understanding, please READ the entire documentation bellow.


## Docs:

Capabilities:

- keeps track of your worked tickets, by counting their total per category:

      1. "resolved"
      2. "wip" - work in progress

- if modied the status of a ticket from "wip" --> "resolved", or viceversa, the counter will update, showing the current values per your update

- once a word doc has been saved on Desktop, with a last paragraph as "wip" or "resolved", CLOSED,  and run the script, the script will:

    1. extract all the paragraphs from the word doc
    2. add them to a .txt file,on a Desktop folder, in a specific format, with the current DATE / TIME when the file was processed
    3. while running, will also check thhough all the .txt files inside the specific folder, and will check for the following:
       
        -- if the ticket status is "wip" / "resolved"

        -- if "wip" - will continue running

        -- if "resolved" will check for 2 conditions:

            A. if  the current date is the same with the date of creation, and if YES, will increase the counter of "resolved" tickets on that current date, keeping the .txt file inside the folder untouched

            B. if the current date is NOT same as the ticket date of creation, the counter will not be affected for TOTAL RESOLVED TICKETS, and the specific ticket(s) will be removed

    4. if a ticket was created a few days ago, and all this time the status was "wip", the counter will keep track of it, and if manually changed the status to "resolved", regardless the creation date, the .txt file will NOT be deleted as of current date, but next day

    5. the docx file with all the info MUST be saved on the  Desktop, and once the script run, will copy all the paragraphs, creating the .txt file, and will be moved into WORK_IN_PROGRESS/ , while the .txt file to "my_tickets/"


## Installation

In order to be run the script, folllow the following steps in order:

1. Clone this repo, using __cmd prompt__:

    a) open cmd prompt

    b) navigate to Desktop PATH
    
    ```bash
    cd Desktop
    ```

    ```bash
    git clone https://github.com/adrianbaltag/ticket_count.git
    ```

  2. Install the dependencies:

    a) open a PowerShell terminal window ==>  cd Desktop

    ```bash
    irm https://astral.sh/uv/install.ps1 | iex   
    ```

    b) adding to your PATH, replace with your username:

    ```bash
    $env:Path = "C:\Users\your_username\.local\bin;$env:Path" 
    ```

    c) check if "uv" installed correctly: should see a version

    ```bash
    uv version
    ```

    d) Install Python  3.13 version and add it to PATH 
          - make sure when installing python, to "add it to PATH" while following the     steps provided by the python installer
      
      Here is the link for download(secured): 🐍[Python.org](Python.org)

      To check if installation was succesful, in CMD Prompt run:

      ```bash
      python --version
      ```

    3. navigate to __TICKET_COUNT__ PATH --> PowerShell:

    ```bash
    cd  Desktop/ticket_count
    ```

    4. Create a virtual environment to install all the dependencies of the script

      ```bash
      uv venv
      ```

    5. Activate the .venv:

      ```bash
      .venv\Scripts\activate
      ```

    6. Install project packages and dependencies:

    ```bash
    uv pip install .
    ```

    7. Run the script:

    ```bash
    python main.py
    ```


  ### IMPORTANT NOTES:

Next time when run it, follow this steps, __at the begging of your shift__, since everything is installed on the machine:


```bash
cd Desktop/ticket_count
.venv\Scripts\activate
python main.py
```

Also, after each ticket worked and save on desktop, make sure to add as a last paragraph:
     
__wip__   or   __resolved__


Then, starting with the next tickets, __AFTER__ each .docx file saved on your Desktop, from  __cmd prompt__,  just:

```bash
python main.py
```


#### Enjoy 😎