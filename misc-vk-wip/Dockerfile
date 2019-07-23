FROM python:3.5.2-alpine

WORKDIR /src

# Add app source files
ADD . /src

#install node modules
#RUN npm install
RUN pip3 install requests

CMD ["python3", "bot.py"]
