FROM python:3

ADD . /chatOpsGitHub

RUN pip install -r /chatOpsGitHub/requirements.txt

WORKDIR /chatOpsGitHub

CMD ["python", "application.py"]
