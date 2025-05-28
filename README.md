# PDF File Scanner
    #### Video Demo:  <URL HERE>
    #### Description:
    This is a command-line Python tool that scans a directory for .pdf files, extracts metadata (like Title and Author), file details (like size and last modified date), and exports the information into either a CSV file or a simplified TXT list.

    I built this project using Python and the pypdf library. It recursively scans all PDFs in a specified folder, reads their metadata, and uses fallback logic to provide readable information even when metadata is missing.

    The project also includes automated tests written with pytest and pytest-mock to ensure core functions behave correctly under different scenarios (e.g., missing metadata, valid files).

    You can choose between a full CSV output with detailed columns or a clean TXT file listing each book in the format:
    Author :— Title

    This was built as part of the CS50 Python final project, and it helped me learn how to:

        Work with file systems and paths using pathlib

        Parse PDF metadata using pypdf

        Write reusable functions for different export formats

        Handle edge cases and fallbacks when metadata is incomplete

        Structure and write automated tests for reliability