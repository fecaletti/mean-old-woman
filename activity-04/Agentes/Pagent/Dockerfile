FROM ubuntu:latest

RUN apt update 
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update

RUN apt install python3.7 -y
RUN apt install python3-pip -y
RUN apt install python3.7-distutils -y
RUN apt install python3.7-dev -y
RUN python3.7 -m pip install setuptools==58
RUN python3.7 -m pip install pade
RUN python3.7 -m pip install generators

COPY main.py pagent/main.py

RUN pade create-pade-db

CMD ["pade", "start_runtime", "--port", "2000", "pagent/main.py"]