# Pseudocode Translator

Made by myself to myself.

<br/>

## How it works

The software receives a path to the pseudocode file, reads the file, parse it into JSON and then turns it into SSMS SQL code and an Excel Data Dictionary.

<br/>

## Functionalities

- [x] Parse pseudocode into JSON
- [x] Generate SQL code
- [ ] Generate Data Dictionary
  - [x] In .xlsx (Excel Spreadsheet)
  - [ ] In .csv (Comma-Separated Values)
  - [ ] In .ods (OpenDocument Spreadsheet)
- [ ] Generate ERD (Entity-Relationship Diagram)
  - [ ] With just the entities
  - [ ] With the complete SQL in a table format

<br/>

## Pseudocode Structure

> If this is too hard to read, see the [example](#example) and the [notes and rules](#notes-and-rules) to learn how to use it.
```
{for each table in the database}
- {table name} {optional: {'// ' or '# ' + table notes}}
  {optional: {'description: ' + table description }}
  {for each attribute in the table}
  - {name} {type}{optional: {'({size})'}} {constrains separated by spaces} {optional: {'// ' or '# ' + description}}
  {end for}
{end for}
```

### Example
```
- user  # Needs to have a special character in the name or the password
  description: Stores the credentials of a user
  - user_id PK
  - name varchar(64)
  - password varchar(256)  // Needs to have at least 8 characters

- data  // References the user table
  description: Stores at maximum 1024 characters of whatever the user wants
  - data_id PK
  - user_id FK(user)
  - content: varchar(1024) null
```

### Notes and Rules
- The Database name is the file name without extension (e.g.: `db.txt` database name is `db`).
- All the words, except description and notes, become lower cased when parsed.
- The `not null` constrain is replaced with `null`, to explicitly state that the attribute can be NULL.
- PKs and FKs are defined without type, but when parsed the type will be INT.
- FKs are defined with the "size" being the name of the referenced table.

<br/>

## License

This project is currently not under any external [license](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
