#How to run locally
1. Make sure you have python 3.13 installed and configured. You can use pyenv to configure what version of python you have installed for the repo directory
2. If you do not have pipenv instlled, run command <pip install pipenv>
3. Once pipenv is successfully install, run pipenv sync to ensure the packages will work properly
4. Run pipenv shell in the repo directory
5. In the pipenv shell, run the command <uvicorn src.main:app --reload>
6. 


Use command 
uvicorn src.main:app --reload 
to load it
