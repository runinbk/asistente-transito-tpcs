from services.document_loader import load_documents

if __name__ == "__main__":
    files = ["documents/test.txt"]
    contents = load_documents(files)

    for idx, content in enumerate(contents):
        print(f"Documento {idx + 1}:")
        print(content)
        print("-" * 40)
