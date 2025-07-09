from path_utils import set_repo_root
set_repo_root()

import os
import shutil
from datetime import datetime
from utils import MAIN_OUTPUT_DIR, ARCHIVE_DIR


def move_csvs_with_structure(source_dir, base_archive_dir):
    # Create archive path with today's date
    today_str = datetime.today().strftime("%Y-%m-%d")
    dated_archive_dir = os.path.join(base_archive_dir, today_str)

    print(f"📁 Archiving all CSVs to: {dated_archive_dir}")
    print(f"📦 Preserving folder structure relative to: {source_dir}")

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(".csv"):
                src_file = os.path.join(root, file)

                # Calculate relative path from source_dir
                rel_path = os.path.relpath(root, source_dir)
                dest_dir = os.path.join(dated_archive_dir, rel_path)
                os.makedirs(dest_dir, exist_ok=True)

                dest_file = os.path.join(dest_dir, file)

                # Optional: rename if filename exists
                if os.path.exists(dest_file):
                    base, ext = os.path.splitext(file)
                    i = 1
                    while os.path.exists(dest_file):
                        dest_file = os.path.join(dest_dir, f"{base}_{i}{ext}")
                        i += 1

                shutil.move(src_file, dest_file)
                print(f"✅ Moved: {src_file} → {dest_file}")

    print("🧹 Archiving complete.")


if __name__ == "__main__":
    move_csvs_with_structure(MAIN_OUTPUT_DIR, ARCHIVE_DIR)
