# Built ONLY from the release's own documented setup at the frozen commit:
#   evaluator.py declares `#!/usr/bin/env python` and Python-2 syntax
#   (ur"..." literals); the README documents no dependency beyond `python`.
#   Usage: evaluator.py <tagged_dataset_path> <prediction_path>
# No auditor-added package.
FROM python:2.7-slim
WORKDIR /wtq
COPY . .
CMD ["python", "evaluator.py", "-h"]
