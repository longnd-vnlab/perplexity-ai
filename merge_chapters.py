
import os
import glob

def merge_chapters():
    output_dir = "mysql_book_extract"
    output_file = "High_Performance_MySQL_4th_Summary.md"

    # Lấy danh sách file md đã sort
    files = sorted(glob.glob(os.path.join(output_dir, "*.md")))

    if not files:
        print("❌ No chapter files found.")
        return

    print(f"found {len(files)} chapters. Merging...")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Title
        outfile.write("# High Performance MySQL, 4th Edition - Summary\n\n")
        outfile.write("> Extracted by Perplexity AI (Gemini 3 Pro)\n\n")
        outfile.write("---\n\n")

        for fpath in files:
            print(f"Processing {os.path.basename(fpath)}...")
            with open(fpath, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write("\n\n---\n\n")

    print(f"✅ Merged into {output_file}")

if __name__ == "__main__":
    merge_chapters()
