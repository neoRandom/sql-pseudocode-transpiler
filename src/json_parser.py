import json


def obj_to_str(
        code_obj: dict[
            str,  # Database Name
            list[  # Table List
                dict[  # Table Object
                    str,  # Name
                    list[  # Attribute List
                        dict[  # Attribute Object
                            str,  # ame
                            str,  # Type
                            str,  # Size
                            list[str]  # Modifiers
                        ]
                    ]
                ]
            ]
        ]
    ) -> str:
    return ""


def transpile(file_path: str) -> bool:
    if file_path.strip() == "":
        raise FileNotFoundError("The file path cannot be null.")

    final_code: str = ""

    json_code: list[
        dict[
            str, 
            int, 
            list[
                dict[
                    str, 
                    str, 
                    str, 
                    list[str]
                ]
            ]
        ]
    ] = list()

    code_obj: dict[
        str,  # Database Name
        list[  # Table List
            dict[  # Table Object
                str,  # Name
                list[  # Attribute List
                    dict[  # Attribute Object
                        str,  # ame
                        str,  # Type
                        str,  # Size
                        list[str]  # Modifiers
                    ]
                ]
            ]
        ]
    ] = dict()

    # Getting the JSON
    json_file = open(file_path, "r", encoding="UTF-8")
    json_code = json.load(json_file)

    # Initializing the code object
    code_obj["database_name"] = file_path.split("/")[-1].split(".")[0]
    code_obj["table_list"] = list()

    # Getting the tables
    for i in range(0):
        # Getting the attributes
        for j in range(0):
            pass
    
    # Converting the code object into a string
    final_code = obj_to_str(code_obj)

    # Saving the SQL
    dot_pos = file_path.rindex(".")
    final_code_path = file_path[0:dot_pos] + ".sql"

    final_code_file = open(final_code_path, "w", encoding="UTF-8")
    final_code_file.write(final_code)

    return True
