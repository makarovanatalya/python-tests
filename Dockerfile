FROM python:3.13-slim-bookworm

ARG TEST_PROFILE=api
ARG SERVER=http://localhost:4111/api
ARG UI_BASE_URL=http://localhost:3000

ENV TEST_PROFILE=${TEST_PROFILE}
ENV SERVER=${SERVER}
ENV UI_BASE_URL=${UI_BASE_URL}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p logs

COPY . .

CMD pytest -m ${TEST_PROFILE} -v --log-level=DEBUG --log-cli-level=DEBUG > logs/run.log 2>&1
