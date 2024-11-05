import pseudocode_parser
import json_parser


if __name__ == "__main__":
    def run():
        file_path = "../build/code.txt"
        output_path: str

        # Pseudocode parsing step
        try:
            print("Parsing the pseudocode as JSON...")
            output_path = pseudocode_parser.transpile(file_path)
        except FileNotFoundError as e:
            print(f"Error: Pseudocode file ´{e.filename}´ not found.\n{e}")
            return
        except Exception as e:
            print(f"Error: Generic error.\n{e}")
            return
        else:
            print("Pseudocode parsed successfully.")
        
        # JSON parsing step
        try:
            print("Parsing the JSON as SQL...")
            json_parser.transpile(output_path)
        except FileNotFoundError as e:
            print(f"Error: JSON file ´{e.filename}´ not found.\n{e}")
            return
        except Exception as e:
            print(f"Error: Generic error.\n{e}")
            return
        else:
            print("JSON parsed successfully.")
    
    run()
