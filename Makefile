export FLASK_APP = app.py

VENV = venv

ACTIVATE = . $(VENV)/bin/activate

all:
	$(ACTIVATE) && flask run

clean:
	rm -rf __pycache__
