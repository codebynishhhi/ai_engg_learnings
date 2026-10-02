from pathlib import Path
import fitz
import re 

def clean_text(text: str) -> str:

    # removea Multiple blank lines
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        # removes Line-level whitespace
        cleaned_line = line.strip()
        cleaned_lines.append(cleaned_line)

    text = "\n".join(cleaned_lines)

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text


def load_text_file(file_path : str) -> str :
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        text = file.read() 

    return clean_text(text)

def load_pdf_file(file_path: str) -> str:
    document = fitz.open(file_path)

    pages = []

    for each_page in document:
        text = each_page.get_text()

        if text:
            pages.append(text)

    document.close()

    return clean_text("\n".join(pages))



if __name__ == "__main__":

    text = load_text_file("documents/sample.txt")
    pdf_text = load_pdf_file("documents/rag_sample.pdf")

    print("===== CLEANED TXT =====")
    print(text)

    print("\n===== CLEANED PDF =====")
    print(pdf_text)


