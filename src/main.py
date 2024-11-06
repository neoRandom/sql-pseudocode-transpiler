import pseudocode_parser
import json_parser
from sys import argv


if __name__ == "__main__":
    def run():
        """
        TODO:
        - Add type hint to pseudocode_parser.py
        - Improve pseudocode_parser.py in general
        - Improve the PK/FK system (in both systems), specially the FK one, 
        to get the referenced table and all that stuff. It will demand a rework
        on the JSON's/Object's structure, like adding a new value to the table
        object saying what table it references, if it has none than it is not an FK.
        - Change the order of the tables to match the dependecy. If the SQL try to
        add a FK to a table that has not been created, it will throw an error.
        """

        file_path: str
        output_path: str

        # Getting the file path
        if len(argv) < 2:
            raise ValueError("Missing required argument: 'file path'")
        file_path = argv[1]

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
