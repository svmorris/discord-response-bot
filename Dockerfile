FROM python:3.10


EXPOSE 5000

WORKDIR /usr/src/app

RUN git clone https://github.com/svmorris/discord-response-bot.git /usr/src/app/

COPY . /usr/src/app/storage

RUN pip install discord
RUN pip install tendo

CMD ["python", "./main.py"]
