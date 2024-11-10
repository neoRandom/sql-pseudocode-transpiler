from models import Attribute, Table, DatabaseSchema
from os.path import exists

class PseudocodeParser:
    def __init__(self, *, update_files: bool = False, verbose_output: bool = False):
        self.update_files = update_files
        self.verbose_output = verbose_output
    
    def transpile(self, file_path: str, output_path: str) -> None:
        """
        Throws:
        - FileNotFoundError
        - OSError
        """
        # If the function should not update the files and the output file exists, cancel the execution
        if not self.update_files and exists(output_path):
            return
        
        if self.verbose_output:
            print("Parsing the pseudocode as JSON...")

        pseudocode_lines: list[str] = list()
        tables_metadata: list[list[int]] = list()
        database: DatabaseSchema = DatabaseSchema.model_construct()

        database.database_name = file_path.split("/")[-1].split(".")[0]
        database.table_list = list()

        # Reading the pseudocode file
        try:
            pseudocode_file = open(file_path, "r", encoding="UTF-8")
        except FileNotFoundError as e:
            # Trust me, this works, it isn't just a dumb code
            # If the open failed, the file isn't open, so it does not require to be closed
            raise FileNotFoundError(e)
        else:
            with pseudocode_file:    
                pseudocode_lines = [
                    line for line in pseudocode_file.readlines()
                    if line.strip() != ""  # Ignores the "\n\n" type of writing, a.k.a. blank line
                ]

        # Getting the code metadata (tables index position and size)
        for i, line in enumerate(pseudocode_lines):
            if line.startswith("  - "):
                tables_metadata[-1][1] += 1
            elif line.startswith("- "):
                tables_metadata.append([i, 0])

        # Getting each table
        for index, size in tables_metadata:
            table: Table = Table.model_construct()
            header_split: list[str]

            # ===== Setting basic informations

            # Getting the header (index)
            header_split = pseudocode_lines[index][2:].split("#")
            if len(header_split) < 2:
                header_split = header_split[0].split("//")
            
            table.name = header_split[0].strip().lower()
            table.notes = header_split[1].strip() if len(header_split) > 1 else "Não se aplica"

            # Getting the description
            if pseudocode_lines[index + 1][2:].lower().startswith("description"):
                table.description = pseudocode_lines[index + 1][2:].split(":")[1].strip()
                index += 1
            else:
                table.description = "Não se aplica"
            
            # Getting the attributes
            table.attribute_list = list()

            for i in range(index + 1, index + size + 1):
                # If it doesnt starts with this, it isnt an attribute
                if not pseudocode_lines[i].startswith("  - "):  
                    continue
                    
                line_split: list[str] 
                attribute: Attribute = Attribute.model_construct()

                # Parsing the line
                line_split = pseudocode_lines[i][4:].split("#")
                if len(line_split) < 2:
                    line_split = line_split[0].split("//")
                
                attr_line = line_split[0].strip().lower()
                attr_line_split = [token.strip() for token in attr_line.replace(", ", ",").split(" ")]
                
                if len(attr_line_split) < 2:  # If it has less than 2 tokens, ignore, it have just the name
                    continue

                attribute.name = attr_line_split[0].replace(":", "")

                if attr_line_split[1] == "unsigned" and len(attr_line_split) > 2:
                    attr_type = attr_line_split[2]
                    attr_line_split = [attr_line_split[0], *attr_line_split[2:]]
                else:
                    attr_type = attr_line_split[1]
                
                if len(attr_line_split) > 2:
                    modifiers = attr_line_split[2:]
                else:
                    modifiers = []

                attribute.description = line_split[1].strip() if len(line_split) > 1 else ""

                if attr_type == "pk" or attr_type.startswith("fk"):
                    # Setting the values on the object
                    attribute.type = "int"  # The default value (for me) of a PK or FK is this
                    attribute.size = ""
                    modifiers.append(attr_type)
                else:
                    # Getting the attribute size if it has one, the value will just be an empty string if not
                    if "(" in attr_type:
                        attr_type, attr_size = attr_type[0:-1].split("(")
                    else:
                        attr_size = ""

                    # If it does not explicitly allows null values, append the `not null` to the modifiers list
                    if "null" not in modifiers:
                        modifiers.append("not null")

                    # Setting the values on the object
                    attribute.type = attr_type
                    attribute.size = attr_size.replace(",", ", ")
                
                attribute.modifiers = [m for m in modifiers] or []
                
                table.attribute_list.append(attribute)
            
            #
            database.table_list.append(table)
        
        # Saving the JSON
        try:
            output_file = open(output_path, "w", encoding="UTF-8")
        except OSError as e:
            raise OSError(e)  # This also isn't a dumb code style
        else:
            with output_file:
                output_file.write(
                    database.model_dump_json(
                        indent=4 
                        if self.verbose_output else None
                    )
                )
        
        if self.verbose_output:
            print("Pseudocode parsed successfully.")
