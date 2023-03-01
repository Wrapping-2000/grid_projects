FROM python:3.9.4

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY post_project_evaluation.py config.py ./
COPY app ./app
COPY boot.sh boot.sh
RUN chmod 755 boot.sh

CMD [ "bash", "boot.sh" ]
