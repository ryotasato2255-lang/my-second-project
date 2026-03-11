from pathlib import Path
from pypdf import PdfReader


def load_documents(data_dir: Path) -> str:
    """Load all .txt and .pdf files from data_dir and return combined text."""
    contents = []

    for path in sorted(data_dir.iterdir()):
        if path.suffix == ".txt":
            text = path.read_text(encoding="utf-8")
            contents.append(f"=== ファイル: {path.name} ===\n{text}")
        elif path.suffix == ".pdf":
            reader = PdfReader(str(path))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n".join(pages)
            contents.append(f"=== ファイル: {path.name} ===\n{text}")

    return "\n\n".join(contents)
