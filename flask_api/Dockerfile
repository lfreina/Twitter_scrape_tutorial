FROM ubuntu:16.04

# get up pip, vim, etc.
RUN apt-get -y update --fix-missing
RUN apt-get install -y python-pip python-dev libev4 libev-dev gcc libxslt-dev libxml2-dev libffi-dev vim curl
RUN pip install --upgrade pip

# get numpy, scipy, scikit-learn and flask
RUN apt-get install -y python-numpy python-scipy
RUN pip install gensim
RUN pip install flask-restful
RUN pip install wtforms
RUN pip install nltk

# add our project
ADD . /

# expose the port for the API
EXPOSE 5000

# run the API 
CMD [ "python", "/api.py" ]