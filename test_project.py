import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from datetime import datetime
import tempfile
import os

from project import scan_pdfs, save_as_csv, save_as_txt


@pytest.fixture
def mock_pdf_file(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%Fake PDF file\n")
    return pdf_path


def test_scan_pdfs_metadata_found(tmp_path, mocker):
    # Create fake PDF
    pdf_path = tmp_path / "doc.pdf"
    pdf_path.write_text("dummy content")

    # Patch PdfReader
    mock_reader = mocker.patch("project.PdfReader")
    mock_instance = MagicMock()
    mock_instance.metadata = MagicMock(title="Test Title", author="Test Author")
    mock_reader.return_value = mock_instance

    result = scan_pdfs(tmp_path)

    assert len(result) == 1
    assert result[0]["Title"] == "Test Title"
    assert result[0]["Author"] == "Test Author"
    assert result[0]["File Name"] == "doc.pdf"
    assert result[0]["File Path"].endswith("doc.pdf")


def test_scan_pdfs_metadata_missing(tmp_path, mocker):
    pdf_path = tmp_path / "no_meta.pdf"
    pdf_path.write_text("no metadata")

    # Patch PdfReader to simulate missing metadata
    mock_reader = mocker.patch("project.PdfReader")
    mock_instance = MagicMock()
    mock_instance.metadata = None
    mock_reader.return_value = mock_instance

    result = scan_pdfs(tmp_path)

    assert result[0]["Title"] == "no_meta"
    assert result[0]["Author"] == ""


def test_save_as_csv(tmp_path):
    data = [
        {
            "File Name": "sample.pdf",
            "File Path": "/fake/path/sample.pdf",
            "Size (MB)": 1.23,
            "Last Modified": "2024-01-01 12:00",
            "Title": "Sample Book",
            "Author": "Author Name",
        }
    ]
    output_file = tmp_path / "output.csv"
    save_as_csv(data, output_file)

    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Sample Book" in content
    assert "Author Name" in content


def test_save_as_txt(tmp_path):
    data = [
        {
            "File Name": "sample.pdf",
            "Title": "Book Title",
            "Author": "Author Name",
        },
        {
            "File Name": "unknown.pdf",
            "Title": "",
            "Author": "",
        },
    ]
    output_file = tmp_path / "output.txt"
    save_as_txt(data, output_file)

    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Author Name :— Book Title" in content
    assert "Unknown :— unknown" in content
