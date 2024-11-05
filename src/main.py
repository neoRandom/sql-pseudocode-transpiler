from pseudocode import transpile


def run():
    file_path = "../build/code.txt"

    try:
        print("Parsing the pseudo-code as JSON...")
        transpile(file_path)
    except FileNotFoundError as e:
        print(f"Error: file ´{e.filename}´ not found")
        return
    else:
        print("Code parsed successfully")


if __name__ == "__main__":
    run()
