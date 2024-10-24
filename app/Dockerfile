FROM python:3.9.20-bookworm
WORKDIR /usr/src/app
RUN apt-get update && apt-get upgrade -y && apt-get install -y python3
COPY ./app.py \
     ./requirements.txt \
     ./
COPY ./assets \
     ./assets
RUN pip install -r ./requirements.txt
RUN chmod +rx ./app.py
ENV PATH="/app:$PATH"
ENV PORT=8050
EXPOSE 8050
ENTRYPOINT ["gunicorn", "app:server", "-b", "0.0.0.0:8050"]