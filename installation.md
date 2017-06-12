# Installation Steps

1. Install **virtualenv** using `pip install virtualenv`
2. Create new *virtual environment folder* using `virtualenv EruditeX(folder name)` command in cmd prompt.
3. Initialise a git repo in folder created above and pull the github repo.
4.  Activate the virtual environment using command `source bin/activate`.
5.  Run `pip install -r requirements.txt`.
6.  To install all of nltk's data, run the command `python -m nltk.downloader all`.
7.  To install spcay english models, run the command `python -m spacy.en.download all`.

**Note:** Execute all codes after activating virtual environment (Step 4). Exit the virtual environment using command `deactivate`, when done.
