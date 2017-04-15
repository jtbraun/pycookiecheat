FROM selenium/standalone-chrome-debug

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install git make build-essential python-dev python-pip libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl
RUN git clone git://github.com/yyuu/pyenv.git /opt/pyenv

ENV PYENV_ROOT /opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# RUN pyenv install 2.7.13
# RUN pyenv install 3.4.2
# RUN pyenv install 3.5.3
RUN pyenv install 3.6.1
# RUN pyenv install pypy2-5.7.0

# RUN pyenv global 3.6.1 3.5.3 3.4.2 2.7.13 pypy2-5.7.0
RUN pyenv global 3.6.1

RUN \
  python3 -m venv venv && \
  venv/bin/python3 -m pip install --upgrade selenium git+https://github.com/n8henrie/pycookiecheat@dev

CMD ["bash"]
