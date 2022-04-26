# start by pulling the python image
FROM python:3.9

# copy every content of the current directory into the image
COPY . /app

# switch working directory
WORKDIR /app

# upgrade pip

RUN pip3 install --upgrade pip

# update setup tools
RUN python3 -m pip install --upgrade setuptools

# install the dependencies and packages from the requirements file
RUN pip3 install -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]