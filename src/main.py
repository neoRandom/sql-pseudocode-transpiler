from multiprocessing import Process
from argument_parser import ArgumentParser
from pseudocode_parser import PseudocodeParser
import json_to_sql
import json_to_excel


HELP_MESSAGE = """
*** SQL Pseudocode Transpiler ***
Description: Transpile a custom SQL pseudocode into JSON, then into multiple things
                  
Options:
  --file-path <path>: Defines the path to the pseudocode file
  --verbose: Turns on the verbose mode (show progress and generate an indented JSON)
  --update: Allows the transpiler to update existent files
"""


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

        # Showing the help
        if args_parser.option_exists("help"):
            print(HELP_MESSAGE)
            return

        # Getting the arguments and options
        file_path = args_parser.get_argument(1, option_key="filepath", error_message="Missing required argument: 'filepath'")
        update_files = args_parser.option_exists("update")
        verbose_output = args_parser.option_exists("verbose")

        # Getting the output path
        json_path = file_path[:file_path.rindex(".")] + ".json"

        # Pseudocode parsing step
        def generate_json() -> bool:
            pseudocode_parser = PseudocodeParser(update_files=update_files, verbose_output=verbose_output)
        
            try:
                pseudocode_parser.transpile(file_path, json_path)
            except FileNotFoundError as e:
                print(f"Error: Pseudocode file ´{e.filename}´ not found.\n{e}")
            except Exception as e:
                print(f"Error: Generic error.\n{e}")
            else:
                return True
            return False
        
        # JSON parsing step
        def generate_sql():
            try:
                print("Parsing the JSON as SQL...")
                json_to_sql.transpile(json_path)
            except FileNotFoundError as e:
                print(f"Error: JSON file ´{e.filename}´ not found.\n{e}")
            except Exception as e:
                print(f"Error: Generic error.\n{e}")
            else:
                print("JSON generated successfully.")

        # Excel step
        def generate_excel_dd():
            try:
                print("Generating the Data Dictionary (Excel)...")
                json_to_excel.parse_json_to_excel(json_path)
            except FileNotFoundError as e:
                print(f"Error: JSON file ´{e.filename}´ not found.\n{e}")
            except Exception as e:
                print(f"Error: Generic error.\n{e}")
            else:
                print("Data Dictionary (Excel) generated successfully.")

        if not generate_json():
            raise RuntimeError("Error generating the JSON file.")
        
        thread_pool: list[Process] = list()
        functions_to_execute = [generate_sql, generate_excel_dd]

        for func in functions_to_execute:
            thread_pool.append(Process(target=func, args=()))
        
        for thread in thread_pool:
            thread.start()
        
        for thread in thread_pool:
            thread.join()

    run()
