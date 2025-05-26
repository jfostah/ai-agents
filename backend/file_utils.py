import os

def save_to_file(filename: str, content: str, folder: str = "outputs") -> str:
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path