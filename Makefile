install: # Install all all dependencies
	@echo "Installing dependencies..."
	python -m pip install --upgrade pip
	pip install --quiet psycopg2 python-decouple faker

test-enums2:
	python src/enums/migrations.py
	python src/main.py

test-enums:
	tail -f /dev/null

test-tables:
	python src/tables/migrations.py
	python src/main.py

test-ints:
	python src/ints/migrations.py
	python src/main.py
