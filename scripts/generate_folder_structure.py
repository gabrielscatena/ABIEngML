import os

def generate_tree(path, depth=0):
    """
    Generate a tree structure of the folder, represented as markdown.

    :param path: Directory to scan
    :param depth: Current depth of the directory in the tree
    :return: A markdown formatted string representing the folder structure
    """
    markdown = ''
    indent = '│   ' * depth
    prefix = '├── ' if depth > 0 else ''
    
    # List all files and directories in the given directory
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return ''
    
    for entry in entries:
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            markdown += f"{indent}{prefix}{entry}/\n"
            markdown += generate_tree(entry_path, depth + 1)
        else:
            markdown += f"{indent}{prefix}{entry}  # {entry}\n"

    return markdown

def save_markdown(directory, output_file="directory_structure.md"):
    """
    Save the generated directory structure in markdown format.

    :param directory: The root directory to scan
    :param output_file: The name of the output markdown file
    """
    tree_structure = generate_tree(directory)
    
    with open(output_file, 'w') as file:
        file.write("# Project Folder Structure\n")
        file.write("```bash\n")
        file.write(tree_structure)
        file.write("```\n")

if __name__ == "__main__":
    repo_root = '.'
    save_markdown(repo_root)
    print(f"Directory structure has been saved to 'directory_structure.md'")
