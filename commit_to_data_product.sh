pip install -r requirements.txt

pytest

git clone # TODO: tics repo - branch megadással

cd tics_repo

python3 generate_notebook.py --file generic_utils.py --folder notebook # TODO: argumentum legyen a két paraméter
python3 generate_notebook.py --file test_descriptor.py --folder notebook
python3 generate_notebook.py --file test_notebook.py --folder notebook
python3 generate_notebook.py --file test_utils.py --folder notebook
python3 generate_notebook.py --file vacuum_notebook.py --folder notebook

git clone ___ # TODO: melyik repot akarom használni
git checkout -b add_generic_utils
git push --set-upstream origin add_generic_utils

cp notebook /generic_utils.json cloned_repo/notebook/generic_utils.json

cd cloned_repo

git add notebooks/generic_utils.json
git commit -m 'add generic utils.json'
git push

#TODO: create a pull request to main
