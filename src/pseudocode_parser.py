import json
from models import Attribute, JSONSchema


def transpile(file_path: str) -> str:
    """
    Throws:
    - OSError
    - FileNotFoundError
    """
    pseudocode_lines: list[str] = list()
    tables_metadata: list[list[int]] = list()
    table_list: list[JSONSchema] = list()

    # Reading the pseudocode file
    pseudocode_file = open(file_path, "r", encoding="UTF-8")
    pseudocode_lines = [
        line for line in pseudocode_file.readlines()
        if line.strip() != ""
    ]

    # Getting the code metadata (tables index position and size)
    for i, line in enumerate(pseudocode_lines):
        if line.startswith("- "):
            tables_metadata[-1][1] += 1
        else:
            tables_metadata.append([i, 0])

    # Getting each table
    for index, size in tables_metadata:
        table: JSONSchema = JSONSchema.model_construct()

        # Setting basic informations
        table.name = pseudocode_lines[index][0:-1].lower()
        table.size = size
        table.body = list()

        # Getting the attributes
        for i in range(index, index + size):
            line = pseudocode_lines[i + 1][2:-1]
            attribute: Attribute = Attribute.model_construct()

            # TODO: Improve the line splitting system, its too bad and leads to errors.
            # Some explanations on how this currently works:
            # - ´replace("unsigned ", "unsigned-")´ is to ignore the type prefix when splitting
            # - ´replace(", ", ",")´ is to ignore the space-separed commas in the type size
            attr_name, attr_type, *modifiers = line.replace("unsigned ", "unsigned-").replace(", ", ",").split(" ")

            attr_name = attr_name.lower().replace(":", "")
            attr_type = attr_type.lower().replace("-", " ")  

            if attr_type == "pk" or attr_type.startswith("fk"):
                # Setting the values on the object
                attribute.name = attr_name
                attribute.type = "unsigned int"  # The default value (for me) of a PK or FK is `unsigned int`
                attribute.size = ""
                attribute.modifiers = [m.lower() for m in modifiers] or []
                attribute.modifiers.append(attr_type)
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
                attribute.name = attr_name
                attribute.type = attr_type
                attribute.size = attr_size.replace(",", ", ")
                attribute.modifiers = [m.lower() for m in modifiers] or []
            
            table.body.append(attribute)
        
        #
        table_list.append(table)
    
    # Saving the JSON
    dot_pos = file_path.rindex(".")
    output_path = file_path[0:dot_pos] + ".json"

    output_file = open(output_path, "w", encoding="UTF-8")
    output_file.write(
        json.dumps(
            [table.model_dump() for table in table_list], 
            indent=4
        )
    )

    return output_path
