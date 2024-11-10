from typing import List, Any, Iterable
from models import Table, DatabaseSchema


def insert_command(
        *sql: Iterable[Any], 
        pad: int = 0, 
        sep: str = ";",
        end: str = ";"
    ) -> str:
    if len(sql) == 0:
        raise RuntimeError("Expected non-empty tuple")
    
    # The separator and the end str always end with a new line
    sep += "\n" 
    end += "\n"

    if isinstance(sql[0], str):
        return sep.join([(" " * pad) + line for line in sql]) + end # type: ignore
    
    return sep.join([(" " * pad) + " ".join(line) for line in sql]) + end


def insert_table(table: Table) -> str:
    table_sql: str = insert_command(
        ("CREATE TABLE", table.name), 
        end=" ("
    )

    attributes_sql: List[Iterable[str]] = list()
    constrains_sql: List[Iterable[str]] = list()
    fk_list: List[tuple[str, str]] = list()

    # Getting the SQL for the beginning part of the inner part of the table, a.k.a. the attributes
    for attribute in table.attribute_list:
        attr_name = attribute.name
        attr_type = attribute.type.upper()
        attr_mods = [m.upper() for m in attribute.modifiers]

        referenced_table: str = ""  # For the FK operation

        for mod in attr_mods:
            if mod.startswith("FK"):
                try:
                    referenced_table = mod.split("(")[1][:-1]
                except IndexError:
                    raise RuntimeError("Expected foreign Table name")
                fk_list.append((attr_name, referenced_table.lower()))
                attr_mods.remove(mod)
                break
            elif mod == "PK":
                attr_mods.remove("PK")
                attr_mods.append("IDENTITY")
                constrains_sql.append(f"PRIMARY KEY ({attr_name})")  # Adding the PRIMARY KEY table constrain
                break
        
        if attribute.size != "":  # If the attribute has a size, append it with parenthesis like a normal SQL
            attr_type += f"({attribute.size})"

        attributes_sql.append(
            (attr_name, attr_type, " ".join(attr_mods)) 
            if attr_mods else 
            (attr_name, attr_type)
        )

    

    # Getting the FOREIGN KEY constrains
    for fk_name, referenced_table in fk_list:
        constrains_sql.append(f"FOREIGN KEY ({fk_name}) REFERENCES {referenced_table}")

    if constrains_sql:
        table_sql += insert_command(*attributes_sql, pad=4, sep=",", end=",\n")
        table_sql += insert_command(*constrains_sql, pad=4, sep=",", end="\n);")
    else:
        table_sql += insert_command(*attributes_sql, pad=4, sep=",", end="\n);")

    return table_sql


def obj_to_str(database_schema: DatabaseSchema) -> str:
    sql: str = ""

    # Defining the database
    sql += insert_command(
        ("CREATE DATABASE", database_schema.database_name),
        ("USE", database_schema.database_name)
    )
    sql += "\n"

    #Defining the tables
    table_list: List[str] = list()

    for table in database_schema.table_list:
        table_list.append(
            insert_command(
                insert_table(table), 
                sep="",
                end=""
            )
        )
    
    sql += "".join(table_list)

    return sql[:-1] if sql[-1] == "\n" else sql


def transpile(file_path: str) -> bool:
    if file_path.strip() == "":
        raise FileNotFoundError("The file path cannot be null.")

    sql_code: str = ""

    database_object: DatabaseSchema = DatabaseSchema.model_construct()

    # Getting the JSON
    try:
        json_file = open(file_path, "r", encoding="UTF-8")
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    else:
        with json_file:
            database_object = DatabaseSchema.model_validate_json(json_file.read())
    
    # Converting the code object into a string
    sql_code = obj_to_str(database_object)

    # Saving the SQL
    dot_pos = file_path.rindex(".")
    final_code_path = file_path[0:dot_pos] + ".sql"

    try:
        final_code_file = open(final_code_path, "w", encoding="UTF-8")
    except OSError as e:
        raise OSError(e)
    else:
        with final_code_file:
            final_code_file.write(sql_code)

    return True
