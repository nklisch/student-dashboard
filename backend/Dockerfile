FROM tiangolo/uvicorn-gunicorn:python3.8

# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create false
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./mypy.ini ./poetry.lock ./pyproject.toml* /app/
COPY ./docker.env /app/.env
RUN poetry install --no-root --no-dev

COPY ./backend /app/app
