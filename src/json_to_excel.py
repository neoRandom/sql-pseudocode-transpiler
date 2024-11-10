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
        obj_rows.append(["Campos"])
        obj_rows.append(["Nome", "Descrição", "Tipo de dado", "Tamanho", "Restrições"])

        for attribute in table.attribute_list:
            attr_name = attribute.name
            attr_type = attribute.type
            attr_size = attribute.size
            modifiers = ", ".join(
                [
                    "FK" if m.startswith("fk")
                    else "PK, Identity" if m == "pk"
                    else m.capitalize()
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

    for row_index in range(2, ws.max_row):
        pattern_fill: opxs.PatternFill
        cells_to_fill: int = 1

        match ws[row_index][0].value:
            case "Tabela" | "Descrição" | "Observações":
                ws.merge_cells(start_row=row_index, start_column=2, end_row=row_index, end_column=5)
                pattern_fill = opxs.PatternFill(start_color="bdd7ee", end_color="bdd7ee", fill_type="solid")
                ws[row_index][1].alignment = opxs.Alignment(horizontal="left", vertical="center", indent=1)
            case "Campos":
                ws.merge_cells(start_row=row_index, start_column=1, end_row=row_index, end_column=5)
                pattern_fill = opxs.PatternFill(start_color="c6e0b4", end_color="c6e0b4", fill_type="solid")
            case "Nome":
                pattern_fill = opxs.PatternFill(start_color="bdd7ee", end_color="bdd7ee", fill_type="solid")
                cells_to_fill = 5
            case _: continue
        
        if ws[row_index][0].value in ("Tabela", "Descrição", "Observações", "Campos", "Nome"):
            font = opxs.Font(b=True)
            alignment = opxs.Alignment(horizontal="center", vertical="center")
            ws.row_dimensions[row_index].height = 20
            for cell_index in range(cells_to_fill):
                ws[row_index][cell_index].font = font
                ws[row_index][cell_index].fill = pattern_fill
                ws[row_index][cell_index].alignment = alignment
    
    # Salvar as alterações
    wb.save(output_file)


def parse_json_to_excel(json_path: str):
    output_file = json_path[:json_path.rfind(".")] + ".xlsx"

    tables = parse_json_to_obj(json_path)
    generate_excel(tables, output_file)

parse_json_to_excel('build/pet.json')
