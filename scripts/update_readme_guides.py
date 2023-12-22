from pathlib import Path

root_dir = Path(__file__).parent.parent
readme = root_dir / "README.md"
guides = root_dir / "docs/guides/"

def get_rst_doc_title(file:Path):
    # in the content of the file, the title is the line above the first line that start with =
    title = ""
    for line in file.read_text().splitlines():
        if line.startswith("="):
            break
        title = line
    return title


def get_guides_list():
    guides_md = []
    for file in guides.iterdir():
        if file.name.startswith("index"):
            continue
        link = f"https://falco.oluwatobi.dev/guides/{file.stem}.html"
        title = get_rst_doc_title(file)
        guides_md.append(f"- [{title}]({link})")


    return "\n" + "\n".join(guides_md) + "\n"


def update_readme(start_comment, end_comment, new_content):
    text = readme.read_text()
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    new_content = text[:start_index] + new_content + text[end_index:]
    readme.write_text(new_content)


def main():
    update_readme(
        "<!-- GUIDES-LIST:START -->",
        "<!-- GUIDES-LIST:END -->",
        get_guides_list(),
    )
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
