from pathlib import Path
import sys

def main() -> None:
    try:
        # Folder where the script is located
        folder = Path(__file__).resolve().parent

        # Output file name = folder name + .txt
        output_path = folder / f"{folder.name}.txt"

        # Collect txt files (case-insensitive), excluding the output file if it already exists
        txt_files = sorted(
            [p for p in folder.iterdir()
             if p.is_file()
             and p.suffix.lower() == ".txt"
             and p.resolve() != output_path.resolve()],
            key=lambda p: p.name.lower()
        )

        print(f"Folder: {folder}")
        print(f"Found {len(txt_files)} .txt files.")
        if not txt_files:
            print("Nothing to do: no .txt files found.")
            return

        print(f"Output will be: {output_path}")

        # Write combined content
        with output_path.open("w", encoding="utf-8", newline="\n") as out:
            for i, path in enumerate(txt_files, start=1):
                print(f"[{i}/{len(txt_files)}] Adding: {path.name}")
                out.write(f"===== FILE: {path.name} =====\n")
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    # Fallback for non-UTF8 text files
                    text = path.read_text(encoding="utf-8", errors="replace")
                out.write(text)
                if not text.endswith("\n"):
                    out.write("\n")
                out.write("\n")

        print("\nDone.")
        print(f"Created: {output_path}")

    except Exception as e:
        print("\nERROR:", repr(e))
        print("If you ran this by double-clicking, errors would normally vanish instantly.")
        print("This script keeps the window open so you can read them.")
        sys.exit(1)

if __name__ == "__main__":
    main()
    input("\nPress Enter to close...")
