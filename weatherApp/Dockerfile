FROM python:3.8-alpine

#RUN apt update
#RUN apt-get install -y python3-pip 
#RUN pip install pipenv

RUN mkdir /home/weather
WORKDIR /home/weather

COPY /requirements.txt /home/weather/
RUN pip3 install -r /home/weather/requirements.txt


COPY /app.py /get_city_info.py /get_forecast_info.py /Pipfile /Pipfile.lock /home/weather/
COPY /templates/index.html /templates/invalid_name.html /templates/result.html /home/weather/templates/
#ENV source /root/.local/share/virtualenvs/weather-MbXMB2yJ
#RUN pip3 install -r /home/weather/requirements.txt

EXPOSE 8989
#to get requests from anywhere via port 8989
CMD gunicorn --bind 0.0.0.0:8989 app:app


