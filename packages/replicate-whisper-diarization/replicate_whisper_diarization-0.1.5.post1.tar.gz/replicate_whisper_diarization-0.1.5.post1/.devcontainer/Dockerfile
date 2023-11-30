# syntax=docker/dockerfile:1.3
FROM ubuntu:22.04 as whisper_diarization-core
ENV EDITOR=vim
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

ARG PYTHON_VERSION=python3.10
ARG PIP_VERSION=23.2.1

# OS packages
# RUN apt-get update --fix-missing; exit 0
RUN apt update && apt install -y --no-install-recommends \
    curl \
    wget \
    git-core \
    htop \
    unzip \
    vim \
    ssh \
    gcc \
    zsh \
    ca-certificates \
    python3-setuptools \
    ${PYTHON_VERSION} \
    ${PYTHON_VERSION}-dev \
    ${PYTHON_VERSION}-distutils \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/tmp/* /var/lib/apt/lists/*

# Set default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/${PYTHON_VERSION} 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/${PYTHON_VERSION} 1


WORKDIR /tmp

# Install pip
RUN wget https://github.com/pypa/pip/archive/refs/tags/${PIP_VERSION}.zip --no-check-certificate \
    && unzip ${PIP_VERSION}.zip \
    && cd pip-${PIP_VERSION} \
    && python setup.py install

FROM whisper_diarization-core as devcontainer

ARG USER_NAME=vscode
ARG USER_UID
ARG USER_GID

RUN groupadd --gid $USER_GID $USER_NAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USER_NAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME \
    && chmod 0440 /etc/sudoers.d/$USER_NAME \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/* \
    && rm -rf /var/lib/apt/lists/*

ENV SHELL=/usr/bin/zsh
RUN chsh $USER_NAME -s $SHELL


RUN --mount=type=cache,target=/root/.cache,id=pip \
    pip install jupyterlab matplotlib seaborn pandas numpy plotly pre-commit

# COPY requirements.txt /workspace/requirements.txt
# RUN --mount=type=cache,target=/root/.cache,id=pip \
#     pip install -r /workspace/requirements.txt

USER $USER_NAME
WORKDIR /tmp
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
