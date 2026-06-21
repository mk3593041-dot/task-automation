"""
Task Automation Scripts — CodeAlpha Task 3
Three automation tools in one file. Run and pick which one to use.
"""

import os
import re
import shutil


# ══════════════════════════════════════════════════════════════════════════════
# AUTOMATION 1 — Move all .jpg files from one folder to another
# ══════════════════════════════════════════════════════════════════════════════

def move_jpg_files(source_folder: str, destination_folder: str) -> None:
    """
    Move every .jpg / .jpeg file from source_folder into destination_folder.
    Creates the destination folder if it doesn't exist.
    """
    # Validate source folder exists
    if not os.path.isdir(source_folder):
        print(f"  ✗ Source folder not found: '{source_folder}'")
        return

    # Create destination folder if needed
    os.makedirs(destination_folder, exist_ok=True)

    # Find all .jpg / .jpeg files (case-insensitive)
    jpg_files = [
        f for f in os.listdir(source_folder)
        if f.lower().endswith((".jpg", ".jpeg"))
    ]

    if not jpg_files:
        print("  ✗ No .jpg files found in the source folder.")
        return

    moved = 0
    for filename in jpg_files:
        src  = os.path.join(source_folder, filename)
        dest = os.path.join(destination_folder, filename)

        # Handle duplicate filenames in destination
        if os.path.exists(dest):
            base, ext = os.path.splitext(filename)
            dest = os.path.join(destination_folder, f"{base}_copy{ext}")

        shutil.move(src, dest)
        print(f"  ✓ Moved: {filename}")
        moved += 1

    print(f"\n  Done! {moved} file(s) moved to '{destination_folder}'")


# ══════════════════════════════════════════════════════════════════════════════
# AUTOMATION 2 — Extract all email addresses from a .txt file
# ══════════════════════════════════════════════════════════════════════════════

def extract_emails(input_file: str, output_file: str) -> None:
    """
    Read input_file, find all email addresses using regex,
    and write unique emails to output_file.
    """
    if not os.path.isfile(input_file):
        print(f"  ✗ File not found: '{input_file}'")
        return

    # Regex pattern for standard email addresses
    email_pattern = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    found = email_pattern.findall(content)

    # Deduplicate while preserving order
    seen   = set()
    unique = []
    for email in found:
        email_lower = email.lower()
        if email_lower not in seen:
            seen.add(email_lower)
            unique.append(email)

    if not unique:
        print("  ✗ No email addresses found in the file.")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Extracted emails ({len(unique)} found)\n")
        f.write("=" * 40 + "\n")
        for email in unique:
            f.write(email + "\n")

    print(f"  ✓ Found {len(unique)} unique email(s):")
    for email in unique:
        print(f"    • {email}")
    print(f"\n  Saved to: '{output_file}'")


# ══════════════════════════════════════════════════════════════════════════════
# AUTOMATION 3 — Scrape a webpage title and save it
# ══════════════════════════════════════════════════════════════════════════════

def scrape_webpage_title(url: str, output_file: str = "scraped_titles.txt") -> None:
    """
    Fetch a webpage and extract its <title> tag content.
    Saves the result to output_file.
    """
    try:
        import urllib.request
    except ImportError:
        print("  ✗ urllib is not available.")
        return

    # Basic title regex (no external dependency needed for simple cases)
    title_pattern = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)

    print(f"  Fetching: {url}")

    try:
        # Add a browser-like User-Agent to avoid 403 blocks
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; PythonScraper/1.0)"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            html = response.read().decode("utf-8", errors="replace")

    except Exception as e:
        print(f"  ✗ Failed to fetch URL: {e}")
        return

    match = title_pattern.search(html)
    title = match.group(1).strip() if match else "No title found"

    # Clean up whitespace / newlines inside the title
    title = " ".join(title.split())

    print(f"  ✓ Title found: {title}")

    # Append result to output file
    from datetime import datetime
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {url}\n")
        f.write(f"Title: {title}\n\n")

    print(f"  Saved to: '{output_file}'")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n╔══════════════════════════════════════╗")
    print("║   Task Automation Scripts v1.0       ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Move .jpg files to a new folder  ║")
    print("║  2. Extract emails from a .txt file  ║")
    print("║  3. Scrape a webpage title           ║")
    print("║  0. Exit                             ║")
    print("╚══════════════════════════════════════╝")

    choice = input("\n  Select an option (0-3): ").strip()

    if choice == "1":
        print("\n── Move .jpg Files ─────────────────────")
        src  = input("  Source folder path: ").strip()
        dest = input("  Destination folder path: ").strip()
        move_jpg_files(src, dest)

    elif choice == "2":
        print("\n── Extract Emails ───────────────────────")
        inp = input("  Input .txt file path: ").strip()
        out = input("  Output file path (e.g. emails.txt): ").strip()
        extract_emails(inp, out)

    elif choice == "3":
        print("\n── Scrape Webpage Title ─────────────────")
        url = input("  Enter URL (e.g. https://example.com): ").strip()
        out = input("  Output file [scraped_titles.txt]: ").strip() or "scraped_titles.txt"
        scrape_webpage_title(url, out)

    elif choice == "0":
        print("\n  Goodbye!\n")
    else:
        print("\n  ✗ Invalid option. Please run again.\n")


if __name__ == "__main__":
    main()
