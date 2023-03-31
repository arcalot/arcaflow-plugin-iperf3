ARG package=arcaflow_plugin_iperf3

# build poetry
FROM quay.io/centos/centos:stream8 as poetry
ARG package
RUN dnf -y module install python39 && dnf -y install python39 python39-pip iperf3

WORKDIR /app

COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN python3.9 -m pip install poetry \
 && python3.9 -m poetry config virtualenvs.create false \
 && python3.9 -m poetry install --without dev \
 && python3.9 -m poetry export -f requirements.txt --output requirements.txt --without-hashes

# run tests
# COPY ${package}/ /app/${package}
# COPY tests /app/tests

# RUN mkdir /htmlcov
# RUN pip3 install coverage
# RUN python3 -m coverage run tests/test_iperf3_plugin.py
# RUN python3 -m coverage html -d /htmlcov --omit=/usr/local/*


# final image
FROM quay.io/centos/centos:stream8
ARG package
RUN dnf -y module install python39 && dnf -y install python39 python39-pip iperf3

WORKDIR /app

COPY --from=poetry /app/requirements.txt /app/
# COPY --from=poetry /htmlcov /htmlcov/
COPY LICENSE /app/
COPY README.md /app/
COPY ${package}/ /app/${package}

RUN python3.9 -m pip install -r requirements.txt

WORKDIR /app/${package}

# ENTRYPOINT ["python3", "iperf3_plugin.py"]
CMD []

LABEL org.opencontainers.image.source="https://github.com/arcalot/arcaflow-plugin-iperf3"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL org.opencontainers.image.title="Arcaflow iperf3 plugin"
LABEL io.github.arcalot.arcaflow.plugin.version="1"
