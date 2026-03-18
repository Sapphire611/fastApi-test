start:
	uvicorn app.main:app --reload

test:
	pytest

install:
	pip install -r requirements.txt

activate:
	@echo "Run this command to activate virtual environment:"
	@echo "source venv/bin/activate"

activate_win:
	@echo "Run this command to activate virtual environment:"
	@echo "venv/Scripts/activate"
