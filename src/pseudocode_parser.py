from models import Attribute, Table, DatabaseSchema


def transpile(file_path: str) -> str:
    """
    Throws:
    - FileNotFoundError
    - OSError
    """
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
        if pseudocode_lines[index + 1][2:].lower()[:10] in ("descricao:", "descrição:"):
            table.description = pseudocode_lines[index + 1][2:].split(":")[1].strip()
            index += 1
        else:
            table.description = "Não se aplica"
        
        # Getting the attributes
        table.attribute_list = list()

        for i in range(index + 1, index + size + 1):
            line_split: list[str] 
            attribute: Attribute = Attribute.model_construct()

            # Parsing the line
            line_split = pseudocode_lines[i][4:].split("#")
            if len(line_split) < 2:
                line_split = line_split[0].split("//")
            
            attr_line = line_split[0].strip().lower()

            # TODO: Improve the line splitting system, its too bad and leads to errors.
            # Some explanations on how this currently works:
            # - ´replace(", ", ",")´ is to ignore the space-separed commas in the type size
            attr_name, attr_type, *modifiers = attr_line.replace(", ", ",").split(" ")

            attr_type = attr_type.replace("-", " ")  

            attribute.name = attr_name.replace(":", "")
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
    dot_pos = file_path.rindex(".")
    output_path = file_path[0:dot_pos] + ".json"
    try:
        output_file = open(output_path, "w", encoding="UTF-8")
    except OSError as e:
        raise OSError(e)  # This also isn't a dumb code style
    else:
        with output_file:
            output_file.write(database.model_dump_json(indent=4))

    return output_path
