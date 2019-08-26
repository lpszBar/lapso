IMAGE_NAME = abelgvidal/lapso

image:
	docker build \
		--build-arg LAPSO_S3_BUCKET_NAME="${LAPSO_S3_BUCKET_NAME}" \
		--build-arg LAPSO_S3_ACCESS_KEY="${LAPSO_S3_ACCESS_KEY}" \
		--build-arg LAPSO_S3_SECRET_ACCESS_KEY="${LAPSO_S3_SECRET_ACCESS_KEY}" \
		. -t $(IMAGE_NAME)

dev: image
	docker run -it --rm -v $(CURDIR):/app -p 5000:5000 -w /app $(IMAGE_NAME)

test: image
	docker run -it --rm -v $(CURDIR):/app -w /app --entrypoint pycodestyle $(IMAGE_NAME) --show-source --show-pep8 --max-line-length=120 /app
	docker run -it --rm -v $(CURDIR):/app -w /app/lapso/tests --entrypoint pytest -e PYTHONPATH=/app/lapso $(IMAGE_NAME) --verbose -p no:warnings

reset-db:
	rm db/lapso.db
