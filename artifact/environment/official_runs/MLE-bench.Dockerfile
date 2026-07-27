# Built ONLY from the release's own documented setup at the frozen commit:
#   README.md "Setup": pip install -e .
# requires-python = ">=3.11" (pyproject.toml). No auditor-added package.
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /mlebench
COPY . .
RUN pip install --no-cache-dir -e .
CMD ["mlebench", "--help"]
