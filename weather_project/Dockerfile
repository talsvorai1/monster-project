FROM python:3.8-alpine

RUN mkdir /home/weather
WORKDIR /home/weather

COPY /requirements.txt /home/weather/
RUN pip3 install -r /home/weather/requirements.txt


COPY /app.py /get_city_info.py /get_forecast_info.py /connection_unittest.py /selenium_negative.py /selenium_positive.py /home/weather/
COPY /templates/index.html /templates/invalid_name.html /templates/result.html /templates/history.html /home/weather/templates/ 


EXPOSE 443
#to get requests from anywhere via port 443
CMD gunicorn --bind 0.0.0.0:443 app:app


