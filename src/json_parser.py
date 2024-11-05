import json


def insert_command(*sql: tuple[str] | list[str] | str, tab: str = 0, end: str = ";\n") -> str:
    if type(sql[0]) is str:
        return (" " * tab) + end.join(sql)
    else:
        return (" " * tab) + end.join([" ".join(line) for line in sql]) + end


def insert_table(
    table: dict[  # Table Object
        str,  # Name
        list[  # Attribute List
            dict[  # Attribute Object
                str,  # Name
                str,  # Type
                str,  # Size
                list[str]  # Modifiers
            ]
        ]
    ]) -> str:
    table_sql: str = insert_command(("CREATE TABLE", table["name"]), end=" (\n")

    attributes_sql: str = ""
    for attribute in table["attribute_list"]:
        if "fk" not in attribute["modifiers"] and "pk" not in attribute["modifiers"]:
            attr_name = attribute["name"]
            attr_type = attribute["type"]
            if attribute["size"] != "":
                attr_type += f"({attribute['size']})"

            attributes_sql += insert_command(
                (attr_name, attr_type, " ".join(attribute["modifiers"])), 
                tab=4,
                end=",\n"
            )

    table_sql += insert_command((f"{attributes_sql})"))

    return table_sql


def obj_to_str(
        code_obj: dict[
            str,  # Database Name
            list[  # Table List
                dict[  # Table Object
                    str,  # Name
                    list[  # Attribute List
                        dict[  # Attribute Object
                            str,  # Name
                            str,  # Type
                            str,  # Size
                            list[str]  # Modifiers
                        ]
                    ]
                ]
            ]
        ]
    ) -> str:
    sql: str = ""

    # Defining the database
    sql += insert_command(
        ("CREATE DATABASE", code_obj["database_name"]),
        ("USE", code_obj["database_name"])
    )
    sql += "\n"

    #Defining the tables
    table_list = list()
    for table in code_obj["table_list"]:
        table_list.append(insert_command(insert_table(table)))
    sql += "\n\n".join(table_list)

    return sql + "\n"


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
                        str,  # Name
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
    for i_table in range(len(json_code)):
        table: dict[
            str,
            list[
                dict[
                    str,
                    str,
                    str,
                    list[str]
                ]
            ]
        ] = dict()
        table["name"] = json_code[i_table]["name"]
        table["attribute_list"] = list()

        # Getting the attributes
        for i_attr in range(json_code[i_table]["size"]):
            table["attribute_list"].append(json_code[i_table]["body"][i_attr])
        
        code_obj["table_list"].append(table)
    
    # Converting the code object into a string
    final_code = obj_to_str(code_obj)

    # Saving the SQL
    dot_pos = file_path.rindex(".")
    final_code_path = file_path[0:dot_pos] + ".sql"

    final_code_file = open(final_code_path, "w", encoding="UTF-8")
    final_code_file.write(final_code)

    return True
