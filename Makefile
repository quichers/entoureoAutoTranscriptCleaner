start-conversation:
	poetry run python -m src.scripts.text_smoother_development

scrap-entoureo:
	poetry run python src/scraping_test_script.py