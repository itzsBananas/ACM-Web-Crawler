FROM python:3.8

# Add code
ADD crawl.py .
ADD generation.py .
ADD score.py .
ADD main.py .

# Update pip
RUN pip install -U pip

# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
COPY requirements.txt ./

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


# Install production dependencies.
RUN set -ex; \
    pip install -r requirements.txt;

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app