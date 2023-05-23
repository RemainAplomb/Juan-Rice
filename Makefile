run-main:
	python main.py

run-backend:
	python Backend_Functionalities.py

conda-env-yml:
	conda env export | grep -v "^prefix: " > environment.yml

conda-req:
	conda list -e > requirements.txt

git-status:
	git status

git-add:
	git add -A

git-commit:
	git commit -m ""

git-push:
	git push

git-revert:
	git revert


