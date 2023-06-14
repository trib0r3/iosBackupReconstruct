# iosBackupReconstruct

Reconstruct the human-readable file structure from decrypted guid-based iOS Backup file structure.

## Usage
```bash
python3 iosBackupRestructure.py ./decrypted-backup ./output
```

## How it works
Script reads the contents of `Manifest.db` file and writes:
- files (type `flags = 1`) under paths in `relativePath` column
- meta-files (column `file`, `flags !=1 `) are stored in directories provided under `relativePath` in files with name: `meta-domain.flags.plist`

