from models import DatabaseSchema
import os
import pandas as pd
import openpyxl as opx
import openpyxl.styles as opxs


def parse_json_to_obj(json_path: str) -> list[list[str]]:
    json_file = open(json_path, 'r', encoding="UTF-8")
    database: DatabaseSchema = DatabaseSchema.model_validate_json(json_file.read())

    obj_rows: list[list[str]] = []

    for table in database.table_list:
        table_name = table.name

        obj_rows.append(["Tabela", table_name])
        obj_rows.append(["Descrição"])
        obj_rows.append(["Observações"])
        obj_rows.append([*(["Campos"] * 5)])
        obj_rows.append(["Nome", "Descrição", "Tipo de dado", "Tamanho", "Restrições"])

        for attribute in table.attribute_list:
            attr_name = attribute.name
            attr_type = attribute.type
            attr_size = attribute.size
            modifiers = ", ".join(
                [
                    m.capitalize() if m != "pk" 
                    else "PK" if not m.startswith("fk") 
                    else "FK" 
                    for m in attribute.modifiers 
                ]
            ) 
            
            # Adiciona os dados da tabela em uma lista
            obj_rows.append([attr_name, "", attr_type, attr_size, modifiers])
        obj_rows.append([""])

    return obj_rows


def generate_excel(tables: list[list[str]], output_file: str) -> None:
    # Creating the DataFrame
    df = pd.DataFrame(tables)
    
    # Creating the Excel file
    if os.path.exists(output_file):
        os.remove(output_file)
    df.to_excel(output_file, index=False, sheet_name="main") # type: ignore
    
    # Opening the Excel file to merge some cells
    wb = opx.load_workbook(output_file)
    ws = wb["main"]

    for row in range(2, len(df) + 2):  # A primeira linha (cabeçalho) é a 1
        if ws[row][0].value in ("Tabela", "Descrição", "Observações"):
            ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=5)
            ws[row][0].fill = opxs.PatternFill(start_color="bdd7ee", end_color="bdd7ee", fill_type="solid")
        elif ws[row][0].value == "Campos":
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
            ws[row][0].fill = opxs.PatternFill(start_color="c6e0b4", end_color="c6e0b4", fill_type="solid")

    # Salvar as alterações
    wb.save(output_file)


def parse_json_to_excel(json_path: str):
    output_file = json_path[:json_path.rfind(".")] + ".xlsx"

    tables = parse_json_to_obj(json_path)
    generate_excel(tables, output_file)

parse_json_to_excel('build/pet.json')
