from pathlib import Path
import fitz

def load_text_file(file_path : str) -> str :
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        text = file.read() 

    return text

def load_pdf_file(file_path: str) -> str:
    document = fitz.open(file_path)

    pages = []

    for each_page in document:
        text = each_page.get_text()

        if text:
            pages.append(text)

    document.close()

    return "\n".join(pages)


if __name__ == "__main__":
    text = load_text_file("documents/sample.txt")
    pdf_text = load_pdf_file("documents/rag_sample.pdf")
    # print(text)
    print(pdf_text)


