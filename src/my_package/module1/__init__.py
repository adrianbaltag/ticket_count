"""__init__.py
This module initializes the my_package module."""

from .count_tickets_status import count_ticket_status
from .delete_resolved_txt import clean_resolved_tickets
from .extract_docx_info import extract_investigation_info
from .move_docx import move_docx
from .nrb_ticket import get_nrb_ticket
from .read_docx import read_docx
from .txt_file import create_or_update_ticket_file, rename_existing_files

__all__ = [
    "count_ticket_status",
    "clean_resolved_tickets",
    "extract_investigation_info",
    "get_nrb_ticket",
    "read_docx",
    "create_or_update_ticket_file",
    "rename_existing_files",
    "move_docx",
]
