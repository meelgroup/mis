FROM ubuntu:16.04 as builder

LABEL maintainer="Mate Soos"
LABEL version="1.0"
LABEL Description="MIS"

# get curl, etc
RUN apt-get update
RUN apt-get install --no-install-recommends -y software-properties-common
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get install --no-install-recommends -y make g++
RUN apt-get install --no-install-recommends -y zlib1g-dev git libboost-dev
RUN apt-get install --no-install-recommends -y git

# build mis
USER root
COPY . /mis
WORKDIR /mis
RUN git checkout https://github.com/meelgroup/muser muser2-dir
RUN make

# set up for running
FROM ubuntu:16.04
RUN apt-get update && apt-get install --no-install-recommends -y python3 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /mis/mis.py /usr/local/bin/
COPY --from=builder /mis/muser2 /usr/local/bin/
COPY --from=builder /mis/togmus /usr/local/bin/
COPY --from=builder /mis/muser2-dir/src/tools/muser2/muser2 /usr/local/bin/
WORKDIR /usr/local/bin/
CMD ["/usr/local/bin/mis.py", "--bin","muser2"]

# --------------------
# HOW TO USE
# --------------------
# on a file:
#    docker run --rm -v `pwd`/formula.cnf:/in msoos/mis /in
