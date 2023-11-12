FROM python:3.8.18
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN apt-get install -y git

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# RUN apt-get install libgl1-mesa-dev

# WORKDIR $HOME
# RUN mkdir workspace

# WORKDIR $HOME/workspace/
# RUN git clone https://github.com/midorigameee/app_image-web.git


