# Built ONLY from the release's own documented setup at the frozen commit:
#   README.md: conda env create -f environment.yml
#              conda activate ds1000-3.10
#              # the test code also needs: pip install datasets tqdm
#              python test_ds1000.py
# No auditor-added package, no PYTHONSAFEPATH normalisation.
FROM continuumio/miniconda3:25.1.1-2
WORKDIR /ds1000
COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "ds1000-3.10", "/bin/bash", "-c"]
RUN pip install datasets tqdm
COPY . .
CMD ["conda", "run", "--no-capture-output", "-n", "ds1000-3.10", "python", "test_ds1000.py", "--model", "codex002"]
