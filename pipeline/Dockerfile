FROM python:3.12-slim

# git and bash are test dependencies, not pipeline dependencies: the supervisor
# that publishes this site is shell, and the only honest way to test a shell
# function that stages, commits and pushes is to run it against a scratch
# repository with a real local remote. Skipping those tests when git is absent
# would recreate the exemption that let an unverified rumour sit on the public
# site for two days (see .github/workflows/tests.yml).
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pipeline/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["bash"]
