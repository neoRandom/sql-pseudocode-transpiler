from pseudocode_parser import PseudocodeParser
import json_to_sql
import json_to_excel
from argument_parser import ArgumentParser


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
        json_path: str

        args_parser = ArgumentParser()

        # Getting the arguments and options
        file_path = args_parser.get_argument(1, option_key="filepath", error_message="Missing required argument: 'filepath'")
        verbose_output = args_parser.option_exists("verbose")
        update_files = args_parser.option_exists("update")

        # Getting the output path
        json_path = file_path[:file_path.rindex(".")] + ".json"

        # Pseudocode parsing step
        pseudocode_parser = PseudocodeParser(update_files=True)

        try:
            pseudocode_parser.transpile(file_path, json_path)
        except FileNotFoundError as e:
            print(f"Error: Pseudocode file ´{e.filename}´ not found.\n{e}")
            return
        except Exception as e:
            print(f"Error: Generic error.\n{e}")
            return

        del pseudocode_parser
        
        # JSON parsing step
        try:
            print("Parsing the JSON as SQL...")
            json_to_sql.transpile(json_path)
        except FileNotFoundError as e:
            print(f"Error: JSON file ´{e.filename}´ not found.\n{e}")
            return
        except Exception as e:
            print(f"Error: Generic error.\n{e}")
            return
        else:
            print("JSON generated successfully.")

        # Excel step
        try:
            print("Generating the Data Dictionary (Excel)...")
            json_to_excel.parse_json_to_excel(json_path)
        except FileNotFoundError as e:
            print(f"Error: JSON file ´{e.filename}´ not found.\n{e}")
            return
        except Exception as e:
            print(f"Error: Generic error.\n{e}")
            return
        else:
            print("Data Dictionary (Excel) generated successfully.")
    
    run()
