import json
import os


def generate_paths():

    current_working_directory = os.getcwd()
    notebooks_path = os.path.join(current_working_directory, 'notebook')
    notebook_py_path = os.path.join(current_working_directory, 'notebook_py')

    full_notebooks_paths = [os.path.join(notebooks_path, notebook)
                            for notebook
                            in os.listdir(notebooks_path)]

    if not os.path.exists(notebook_py_path):
        os.mkdir(notebook_py_path)

    return full_notebooks_paths, notebook_py_path


def read_json_file(notebook_path: str) -> dict:

    with open(notebook_path, encoding='utf-8') as notebook_file:
        json_file_content = json.loads(notebook_file.read())

    return json_file_content


def write_py_file(value: list, py_path: str) -> None:

    with open(py_path, 'w', encoding='utf-8') as py_file:
        for line in value:
            py_file.write(line)
            py_file.write(os.linesep)


def process_json_content(json_file_content: dict) -> list:

    code = json_file_content.get('properties').get('cells')
    code_cells = ['\n'.join(code_cell.get('source'))
                  for code_cell
                  in code
                  if code_cell.get('cell_type') == 'code']

    value = '\n'.join(code_cells).split('\n')

    return value


def create_py_file(notebook_path: str, notebook_py_path: str) -> None:

    json_file_content = read_json_file(notebook_path)

    value = process_json_content(json_file_content)
    file_name = notebook_path.split('/')[-1].replace('.json', '.py')

    write_py_file(value, os.path.join(notebook_py_path, file_name))


def main():
    full_notebooks_paths, notebook_py_path = generate_paths()
    for notebook_path in full_notebooks_paths:
        create_py_file(notebook_path, notebook_py_path)


if __name__ == '__main__':
    main()


# TODO: remove the first whitespace before the rows if there is only one
