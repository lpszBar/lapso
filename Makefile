IMAGE_NAME = abelgvidal/lapso

export REGISTRY_USER
export REGISTRY_PASSWORD

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

login:
	@docker login -u="$(REGISTRY_USER)" -p="$(REGISTRY_PASSWORD)"

push: test login imagefresh  ## Push image to registry
	@docker push $(IMAGE_NAME)

deploy: push  ## Deploy 
	ssh -t root@172.104.251.194 'docker stop lapso ||  mkdir -p /opt/lapso-db && touch /opt/lapso-db/lapso.db && docker run --rm -it --name=lapso -d -p 80:80 -v=/opt/lapso-db/lapso.db:/app/db/lapso.db $(IMAGE_NAME):latest'

imagefresh:  ## Build a fresh image
	@docker build --no-cache \
		--build-arg LAPSO_S3_BUCKET_NAME="${LAPSO_S3_BUCKET_NAME}" \
		--build-arg LAPSO_S3_ACCESS_KEY="${LAPSO_S3_ACCESS_KEY}" \
		--build-arg LAPSO_S3_SECRET_ACCESS_KEY="${LAPSO_S3_SECRET_ACCESS_KEY}" \
		. -t $(IMAGE_NAME)

image:	 ## Build an image 
	@docker build \
		--build-arg LAPSO_S3_BUCKET_NAME="${LAPSO_S3_BUCKET_NAME}" \
		--build-arg LAPSO_S3_ACCESS_KEY="${LAPSO_S3_ACCESS_KEY}" \
		--build-arg LAPSO_S3_SECRET_ACCESS_KEY="${LAPSO_S3_SECRET_ACCESS_KEY}" \
		. -t $(IMAGE_NAME)

dev:    ## Run development server
	@docker run -it --rm -v $(CURDIR):/app -p 5000:5000 -p 3000:3000 -w /app $(IMAGE_NAME)

test: image	 ## Run tests
	@docker run -it --rm -v $(CURDIR):/app -w /app --entrypoint pycodestyle $(IMAGE_NAME) --show-source --max-line-length=120 /app
	@docker run -it --rm -v $(CURDIR):/app -w /app/lapso/tests --entrypoint pytest -e PYTHONPATH=/app/lapso $(IMAGE_NAME) --verbose -p no:warnings

reset-db:	## Reset database
	@rm db/lapso.db

shell: image    ## Get a shell in the image
	@docker run -it --rm -v $(CURDIR):/app -w /app/lapso/ --entrypoint sh -e PYTHONPATH=/app/lapso $(IMAGE_NAME)

python: image	## Get a python REPL in the image
	@docker run -it --rm -v $(CURDIR):/app -w /app/lapso/ --entrypoint python -e PYTHONPATH=/app/lapso $(IMAGE_NAME)
