
#
# Description: Makefile 
# Author: Thomas Garvey
#

setup: 
	@echo "Setting up..."
	@python3 -m venv venv
	@echo "Virtual environment created." 
	@venv/bin/pip install -r requirements.txt
	@for i in 1 2 3 4 5; do\
		echo "."; \
	done
	@venv/bin/python setup.py
	@echo "Validating path and creating database (RapidFire.db)..."
	@venv/bin/python validate.py


run:
	@venv/bin/python validate.py
	@venv/bin/python main.py


# save:
# 	@echo "Saving to Hugging Face"
# 	@hf upload tgarvs/RapidFire RapidFire.db  --repo-type=dataset
	

