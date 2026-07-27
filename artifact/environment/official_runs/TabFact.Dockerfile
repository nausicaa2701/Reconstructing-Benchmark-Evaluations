# Built ONLY from the release's own documented setup at the frozen commit:
#   README.md "Requirements": Python 3.5, Ujson, Pytorch 1.2.0, Pandas, tqdm,
#   TensorboardX, unidecode, nltk.  Documented command:
#     cd code/ && python model.py --do_test --resume
#   using the pre-trained checkpoints the release ships in code/checkpoints/.
# Python 3.6 is the oldest base with torch 1.2.0 wheels; the release pins no
# base image. No auditor-added package beyond the documented list.
FROM python:3.6-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir torch==1.2.0 ujson pandas tqdm tensorboardX unidecode nltk numpy
WORKDIR /tabfact
COPY code /tabfact/code
COPY preprocessed_data_program /tabfact/preprocessed_data_program
COPY tokenized_data /tabfact/tokenized_data
COPY data /tabfact/data
WORKDIR /tabfact/code
CMD ["python", "model.py", "--do_test", "--resume"]
