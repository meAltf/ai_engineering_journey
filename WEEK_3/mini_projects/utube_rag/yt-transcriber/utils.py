import os

def save_text(text, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename + ".txt")

    with open(file_path, "w") as f:
        f.write(text)

    return file_path