FROM ubuntu:xenial

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -q && \
    apt-get install -qy locales build-essential wget libfontconfig1 python3 python3-pip poppler-utils vim && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install sphinx ged4py pylatex pdf2image python-dateutil && \
    locale-gen en_US.UTF-8

ENV PATH="/usr/local/texlive/2019/bin/x86_64-linux:${PATH}"
ENV LANG en_US.UTF-8

RUN wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz && \
    mkdir /install-tl-unx && \
    tar -xf install-tl-unx.tar.gz -C /install-tl-unx --strip-components=1 && \
    echo "selected_scheme scheme-basic" >> /install-tl-unx/texlive.profile && \
    /install-tl-unx/install-tl -profile /install-tl-unx/texlive.profile && \
    rm -r /install-tl-unx install-tl-unx.tar.gz && \
    tlmgr install latexmk standalone xkeyval genealogytree tcolorbox pgf xcolor environ trimspaces etoolbox collection-fontsrecommended
