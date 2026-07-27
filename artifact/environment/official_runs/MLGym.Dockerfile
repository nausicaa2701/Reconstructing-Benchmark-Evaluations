# Built ONLY from the release's own documented setup at the frozen commit:
#   pyproject.toml requires-python and dependencies; the per-task scorer
#   data/blotto/evaluate.py imports only json/random/numpy plus the task's
#   own strategy.py and target.py, both shipped by the release.
FROM python:3.11-slim
WORKDIR /mlgym
COPY pyproject.toml ./
COPY data/blotto /mlgym/data/blotto
RUN pip install --no-cache-dir numpy
WORKDIR /mlgym/data/blotto
CMD ["python", "evaluate.py"]
