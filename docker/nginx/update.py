from pathlib import Path
from tools.discussion import discussion
import shutil
import os
import json


CURRENT_BOOK = "project_hail_mary"

SRC_ROOT_PATH = Path(f"/opt/temp_external")
SERVE_ROOT_PATH = Path("/data")
STATUS_PATH = Path("/opt/book_status.json")

def main():
    book_status = json.loads(STATUS_PATH.read_text())

    prev_section = book_status["current_section"]
    max_section = book_status["max_section"]

    next_section = prev_section + 1

    if next_section >= max_section:
        raise Exception("Already at max section, need to switch books!")

    d = discussion(SRC_ROOT_PATH, CURRENT_BOOK)
    # d.process_section(next_section)

    print("=======================================================================================================")

    print(f"Moving updated section {next_section} to serve location...")
    for item in SERVE_ROOT_PATH.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # Bring txt pages + index.json + summary.txt over
    shutil.copytree(
        SRC_ROOT_PATH / "books" / CURRENT_BOOK / f"{CURRENT_BOOK}_text" / f"section_{next_section}/",
        SERVE_ROOT_PATH, dirs_exist_ok=True)

    # Bring over posts.json
    shutil.copy(SRC_ROOT_PATH / "posts" / f"section_{next_section}" / f"post_{next_section}.json", SERVE_ROOT_PATH / "posts.json")
    

if __name__ == "__main__":
    main()