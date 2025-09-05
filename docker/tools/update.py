from pathlib import Path
from tools.discussion import discussion
import shutil
import argparse
import json


def main():
    if SRC_ROOT_PATH.exists():
        shutil.rmtree(SERVE_ROOT_PATH)
        SRC_ROOT_PATH.mkdir(parents=True, exist_ok=True)
    
    book_status_path = SRC_ROOT_PATH / "book_status.json"
    book_status = json.loads(book_status_path.read_text())

    prev_section = book_status["current_section"]
    current_book = json.loads((SRC_ROOT_PATH / "books" / "books.json").read_text())[book_status["book_idx"]]
    print(f"Current book: {current_book}")

    if not TRANSFER_ONLY:
        # Skip generation if just transferring

        max_section = book_status["max_section"]

        next_section = prev_section + 1

        if next_section > max_section:
            print("Past max section, switching books!")
            next_section = 1
            book_status["book_idx"] += + 1

        d = discussion(SRC_ROOT_PATH, current_book)
        d.process_section(next_section)

        print("=======================================================================================================")
    else:
        next_section = prev_section

    print(f"Moving section {next_section} to serve location...")

    # Bring txt pages + index.json + summary.txt over
    shutil.copytree(
        SRC_ROOT_PATH / "books" / current_book / f"{current_book}_text" / f"section_{next_section}/",
        SERVE_ROOT_PATH, dirs_exist_ok=True)

    # Bring over posts.json
    shutil.copy(SRC_ROOT_PATH / "posts" / f"section_{next_section}" / f"post_{next_section}.json", SERVE_ROOT_PATH / "posts.json")
    
    if not TRANSFER_ONLY:
        # Update status file
        book_status["current_section"] = next_section
        book_status_path.write_text(json.dumps(book_status, indent=4))


if __name__ == "__main__":
    global SRC_ROOT_PATH, SERVE_ROOT_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--transfer-only", action="store_true")
    args = parser.parse_args()

    TRANSFER_ONLY = args.transfer_only
    if args.local:
        SRC_ROOT_PATH = Path("../temp_external")
        SERVE_ROOT_PATH = Path("/Users/andrechang/TEMP/data")
    else:
        SRC_ROOT_PATH = Path("/opt/external_volume")
        SERVE_ROOT_PATH = Path("/data")

    main()