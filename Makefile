run-api:
	uvicorn apps.api.main:app --reload --port 8000
run-web:
	cd apps/web && npm run dev
test:
	pytest -q
