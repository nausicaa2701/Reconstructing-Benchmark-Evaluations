# Built ONLY from the release's own documented setup at the frozen commit:
#   cert/pandas-numpy-eval/README.md: "Make sure to use python 3.7 or later"
#   $ pip install -e pandas-numpy-eval
#   $ evaluate_functional_correctness <samples_path>
# No auditor-added package; the shipped example sample file is the input.
FROM python:3.7-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /cert
COPY cert/pandas-numpy-eval /cert/pandas-numpy-eval
RUN pip install --no-cache-dir -e pandas-numpy-eval
WORKDIR /cert/pandas-numpy-eval
CMD ["evaluate_functional_correctness", "data/Example_Pandas_PYCODEGPT_samples.jsonl"]
