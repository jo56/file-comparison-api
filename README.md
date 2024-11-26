#How to run locally
1. Make sure you have python 3.13 installed and configured. You can use pyenv to configure what version of python you have installed for the repo directory
2. If you do not have pipenv instlled, run command <pip install pipenv>
3. Once pipenv is successfully install, run pipenv sync to ensure the packages will work properly
4. Run pipenv shell in the repo directory
5. In the pipenv shell, run the command <uvicorn src.main:app --reload>. You should see a message  Uvicorn running on http://127.0.0.1:8000. This means that the API is running locally
6. You should be able to verify the api is running locally by hitting http://127.0.0.1:8000/{endpoint}

