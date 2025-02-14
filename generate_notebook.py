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
			"enableDebugMode": False,
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
			{
				"cell_type": "code",
				"source": [
                    ""
				],
				"execution_count": None
			}
		]
	}
}

def read_py_file(py_file_name: str = "generic_utils.py"):
    code = []
    with open(py_file_name, "r") as py_file:
        for line in py_file:
            if line.startswith('from generic_utils import ') or line.startswith('import generic_utils'):
                code.append('%run /generic_utils')
            else:
                code.append(line)
    return code


def add_code_to_notebook_outline(notebook_outline_dict: dict, code: list):
    notebook_outline_dict["properties"]["cells"][0]["source"].extend(code)
    notebook_outline_dict["properties"]["cells"][0]["source"].pop(0)
    return notebook_outline_dict


def create_notebook_json(notebook_content: dict, folder: str = "notebook", notebook_name: str = "generic_utils"):
    notebook_content["name"] = notebook_name
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"{notebook_name}.json"), "w") as notebook:
        json.dump(notebook_content, notebook, indent = 4)


def main(py_file_name: str = "generic_utils.py", folder: str = "notebook"):
    code = read_py_file(py_file_name = py_file_name)
    notebook_content = add_code_to_notebook_outline(notebook_outline_dict = notebook_outline_dict, code = code)
    notebook_name = py_file_name.replace('.py', '')
    create_notebook_json(notebook_content = notebook_content, folder = folder, notebook_name = notebook_name)


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
 