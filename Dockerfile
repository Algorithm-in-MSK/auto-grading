FROM python:3.6
LABEL maintainer="seokchan.ahn@kaist.ac.kr"

RUN apt-get update && apt-get install -y sudo

WORKDIR workspace
ADD requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN rm requirements.txt

#ADD wait-for-it.sh .
#RUN chmod 777 wait-for-it.sh