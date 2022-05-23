## Job Tracker Webapp

A web app that allows students to track their internship/job hunting efforts. The target users would be CS students who are attempting to land internships and full time positions upon graduation.

## Getting started

Create a virtual environment

`python3 -m venv venv`

Activate virtual environment

`source venv/bin/activate`

Install packages with requirements.txt

`pip install -r requirements.txt`

Create a directory called "private" in the project directory

`mkdir private`

Include `credentials.json` in the `private` directory.

Include `jobtrack-pyrebase-credentials.json` in the `private` directory.

Run the application locally

`python3 main.py`

## Building and running with Docker

Install Docker from https://docs.docker.com/get-docker/

Build the image by running `docker image build -t jobtracker .`

Run the container by running `docker run -p 5000:5000 -d jobtracker`

Open your web browser and navigate to http://localhost:5000/

## Deploying to Heroku

Login to Heroku: `heroku login`

Build the image: `docker buildx build --platform linux/amd64 -t jobtracker .`

Tag the image: `docker tag jobtracker registry.heroku.com/jobtracker-467/web`

Push the image: `docker push registry.heroku.com/jobtracker-467/web`

Release: `heroku container:release web -a jobtracker-467`
