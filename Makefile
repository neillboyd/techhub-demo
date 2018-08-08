.PHONY: help run build build-production test deploy pull-images push-image

build: ## builds the application
	docker build --force-rm -t techhubtest .

run: ## runs the api
	docker run -ti -p 1200:80 techhubtest:latest

test-perf: ## runs the performance tests via docker compose
	docker-compose -f docker-compose-perf.yml up --exit-code-from k6

test-contract: ## runs the pact contract tests via docker compose
	docker-compose -f docker-compose-pactverify.yml up --exit-code-from pactverifier
