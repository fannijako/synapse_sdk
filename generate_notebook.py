import argparse
import json
import os


notebook_outline_dict = {
	"name": "",
	"properties": {
		"nbformat": 4,
		"nbformat_minor": 2,
		"metadata": {
			"saveOutput": True,
			"enableDebugMode": True,
			"kernelspec": {
				"name": "synapse_pyspark",
				"display_name": "Synapse PySpark"
			},
			"language_info": {
				"name": "python"
			},
			"sessionKeepAliveTimeout": 30
		},
		"cells": [
		]
	}
}

def read_py_file(py_file_name: str = "generic_utils.py"):
    code = []
    with open(py_file_name, "r", encoding='utf-8') as py_file:
        for line in py_file:
            is_from_generic = line.startswith('from generic_utils import ')
            is_generic = line.startswith('import generic_utils')

            is_from_test_helper = line.startswith('from test_helper import ')
            is_test_helper = line.startswith('import test_helper')

            if is_from_generic or is_generic:
                code.append('%run generic_utils')
            elif is_from_test_helper or is_test_helper:
                code.append('%run test_helper')
            elif line.startswith('import mssparkutils'):
                pass
            else:
                code.append(line)
    return code


def split_magic_commands(code: list) -> list:

    splitted_code = []
    current_block = []

    for item in code:
        if item == '%run /generic_utils':
            if current_block:
                splitted_code.append(current_block)
                current_block = []
            splitted_code.append([item])
        else:
            current_block.append(item)

    if current_block:
        splitted_code.append(current_block)

    return splitted_code


def add_code_to_notebook_outline(notebook_outline: dict, code: list):

    for code_block in split_magic_commands(code):

        if code_block[0] in ["\n", ""]:
            code_block = code_block[1:]
        if code_block[-1] in  ["\n", ""]:
            code_block = code_block[:-1]

        notebook_outline["properties"]["cells"].append(
        {
				"cell_type": "code",
				"source": code_block,
				"execution_count": None
			}
        )

    return notebook_outline


def create_notebook_json(notebook_content: dict,
                         folder: str = "notebook",
                         notebook_name: str = "generic_utils"):

    notebook_content["name"] = notebook_name
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, f"{notebook_name}.json"), "w", encoding='utf-8') as notebook:
        json.dump(notebook_content, notebook, indent = 4)


def main(py_file_name: str = "generic_utils.py", folder: str = "notebook"):
    code = read_py_file(py_file_name = py_file_name)
    notebook_content = add_code_to_notebook_outline(notebook_outline_dict, code)
    notebook_name = py_file_name.replace('.py', '')
    create_notebook_json(notebook_content, folder, notebook_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Python file to notebook format')
    parser.add_argument('py_file_name',
                        type = str,
                        nargs = '?',
                        default = 'generic_utils.py',
                        help = 'Python file name to convert (e.g. generic_utils.py)')
    parser.add_argument('folder',
                        type = str,
                        nargs = '?',
                        default='notebook',
                        help = 'Subfolder to place the result to (recommended: notebook)')

    args = parser.parse_args()
    main(py_file_name = args.py_file_name, folder = args.folder)
