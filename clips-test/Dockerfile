FROM ubuntu:latest

WORKDIR /Users/fefo/Projects/UERGS/iA/mean-old-woman/clips-test

COPY . .

RUN apt update && apt upgrade -y
RUN apt install build-essential -y
RUN apt install wget -y
RUN apt install unzip -y
# RUN apt install libclips libclips-dev -y
RUN apt install python3 python3-pip -y

# Download and install CLIPS packages via dpkg
RUN wget http://ftp.br.debian.org/debian/pool/main/c/clips/libclips_6.30-4.1_arm64.deb
RUN wget http://ftp.br.debian.org/debian/pool/main/c/clips/libclips-dev_6.30-4.1_arm64.deb
RUN dpkg -i libclips_6.30-4.1_arm64.deb libclips-dev_6.30-4.1_arm64.deb
RUN rm libclips_6.30-4.1_arm64.deb libclips-dev_6.30-4.1_arm64.deb

WORKDIR /Users/fefo/Projects/UERGS/iA/mean-old-woman/clips-test/clipspy

RUN make
RUN make install

RUN apt upgrade -y

WORKDIR /Users/fefo/Projects/UERGS/iA/mean-old-woman/clips-test/

CMD [ "python3", "./clips_test.py" ]