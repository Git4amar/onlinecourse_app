# pull latest python base image
FROM python:latest

# set working directory
WORKDIR /home/onlinecourse_app
# make directories for static and media files
#RUN mkdir ./staticfiles &&\
#    mkdir ./mediafiles

# upgrade pip and install depedencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project file
COPY . .