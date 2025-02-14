FROM kbase/sdkpython:3.8.0

#FROM kbase/sdkbase2:python
LABEL KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get update && apt-get install -y \
    g++ \
    make \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/mourisl/Lighter.git \
    && cd Lighter \
    && make \
    && cp lighter /usr/local/bin



# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]

