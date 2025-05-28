import argparse
import csv
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader


def main():
    args = parse_args()

    if args.simple and args.output == "pdf_library.csv":
        args.output = "pdf_list.txt"

    if not Path(args.dir).is_dir():
        print(f"❌ Error: Directory '{args.dir}' does not exist.")
        return

    pdf_data = scan_pdfs(args.dir)

    if args.simple:
        save_as_txt(pdf_data, args.output)
    else:
        save_as_csv(pdf_data, args.output)


def parse_args():
    parser = argparse.ArgumentParser(description="Record your PDF's")
    parser.add_argument("--dir", required=True, help="File Directory to Scan")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Save as a simple TXT file with Title and Author only",
    )
    parser.add_argument(
        "--output", default="pdf_library.csv", help="Output CSV File Name"
    )
    return parser.parse_args()


def scan_pdfs(directory):
    print(f"\n📂 Scanning folder: {directory}")
    pdf_files = Path(directory).rglob("*.pdf")
    results = []

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(str(pdf_path))
            info = reader.metadata
            title = info.title if info and info.title else pdf_path.stem
            author = info.author if info and info.author else ""
        except Exception as e:
            print(f"⚠️  Could not read metadata for {pdf_path.name}: {e}")
            title, author = author = pdf_path.stem, ""

        stats = pdf_path.stat()
        size_mb = round(stats.st_size / (1024 * 1024), 2)
        modified_time = datetime.fromtimestamp(stats.st_mtime).strftime(
            "%Y-%m-%d %H:%M"
        )

        results.append(
            {
                "File Name": pdf_path.name,
                "File Path": str(pdf_path.resolve()),
                "Size (MB)": size_mb,
                "Last Modified": modified_time,
                "Title": title,
                "Author": author,
            }
        )

    return results


def save_as_csv(data, output_file):
    print(f"\n💾 Saving to: {output_file}")
    if not data:
        print("⚠️  No data to write.")
        return

    headers = [
        "File Name",
        "File Path",
        "Size (MB)",
        "Last Modified",
        "Title",
        "Author",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ CSV file written: {output_file} ({len(data)} PDF(s))")


def save_as_txt(data, output_file):
    print(f"\n📝 Saving simple list to: {output_file}")
    if not data:
        print("⚠️  No data to write.")
        return

    with open(output_file, "w", encoding="utf-8") as file:
        for entry in data:
            title = entry["Title"] or entry["File Name"]
            author = entry["Author"] or "Unknown"
            file.write(f"{author} :— {title} \n")

    print(f"✅ Text file written: {output_file} ({len(data)} book(s))")


if __name__ == "__main__":
    main()
