FROM python:3.11-slim

ARG SPARK_VERSION=3.5.5
ARG HADOOP_VERSION=3
ARG SPARK_ARCHIVE="spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"
ARG SPARK_URL="https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_ARCHIVE}"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates openjdk-21-jre procps tini git \
    iproute2 iputils-ping net-tools netcat-openbsd \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN node -v && npm -v && npx -v

RUN groupadd -r spark && useradd -m -r -g spark spark

RUN mkdir -p /opt \
    && curl -fsSL ${SPARK_URL} -o /tmp/${SPARK_ARCHIVE} \
    && tar -xzf /tmp/${SPARK_ARCHIVE} -C /opt \
    && ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm /tmp/${SPARK_ARCHIVE}

ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"
ENV PYSPARK_PYTHON=python3
ENV PYTHONUNBUFFERED=1

WORKDIR /workspaces

RUN pip install --no-cache-dir ipython pyspark==${SPARK_VERSION} jupyterlab black pytest
ARG USER_UID=1000
ARG USER_GID=1000
USER spark

EXPOSE 4040 7077 8080 8888
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD [ "bash" ]
