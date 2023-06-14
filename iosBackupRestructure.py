from sys import argv
import os
import sqlite3
import shutil

def process_backup(backup_dir: str, output_dir: str) -> None:
    manifest_path = os.path.join(backup_dir, "Manifest.db")
    if not os.path.exists(manifest_path):
        print("Can't find Manifest.db in backup dir!")
        return
    
    db_connection = sqlite3.connect(manifest_path)
    db_cursor = db_connection.cursor()
    file_list = db_cursor.execute("select fileID, relativePath from Files where flags=1").fetchall()
    for entry in file_list:
        file_id, relative_file_path = entry
        relative_dir = os.path.dirname(relative_file_path)
        os.makedirs(os.path.join(output_dir, relative_dir), exist_ok=True)
        
        original_path = os.path.join(backup_dir, file_id[:2], file_id)
        destination_path = os.path.join(output_dir, relative_file_path)
        shutil.copy2(src=original_path, dst=destination_path)
    print("[*] Copied Files to destination path!")

    metafiles = db_cursor.execute("select fileID, relativePath, domain, file, flags from Files where flags!=1").fetchall()
    for entry in metafiles:
        file_id, relative_path, domain, file_data, flags = entry
        relative_dir = os.path.dirname(relative_path)
        os.makedirs(os.path.join(output_dir, relative_dir), exist_ok=True)
        fname = f"meta-{domain}.{flags}.plist"
        destination_path = os.path.join(output_dir, relative_dir, fname)
        with open(destination_path, "wb") as f:
            f.write(file_data)
    print("[*] Saved Meta-Files to destination path!")
    db_connection.close()


def main() -> None:
    if len(argv) != 3:
        print(f"USAGE: ./{argv[0]} /path/to/decrypted/backup /output/directory")
        return
    
    backup = argv[1]
    output = argv[2]
    if not os.path.exists(backup) or (os.path.exists(output) and len(os.listdir(output)) > 0):
        print("Invalid backup directory or not empty output directory:", backup)
        return
    
    os.makedirs(output, exist_ok=True)
    process_backup(backup_dir=backup, output_dir=output)


if __name__ == "__main__":
    main()
