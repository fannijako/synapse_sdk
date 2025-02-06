git clone # TODO: tics repo - branch megadással

cd tics_repo

python3 generate_notebook.py # TODO: argumentum legyen a két paraméter

git clone ___ # TODO: melyik repot akarom használni
git checkout -b add_generic_utils
git push --set-upstream origin add_generic_utils

cp notebook /generic_utils.json cloned_repo/notebook/generic_utils.json

cd cloned_repo

git add notebooks/generic_utils.json
git commit -m 'add generic utils.json'
git push

#TODO: create a pull request to main
