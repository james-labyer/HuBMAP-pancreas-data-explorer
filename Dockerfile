FROM python:3.9.20-bookworm
RUN apt-get update && apt-get upgrade -y && apt-get install -y python3
RUN pip install pandas==2.2.3 numpy==1.26.4 dash==2.8.1 plotly==5.24.1 dash-bootstrap-components==1.6.0 dash-slicer==0.3.1 cmake gunicorn bioio==1.1.0 bioio-czi==1.0.1
COPY ./ /code/
RUN chmod +rx /code/app.py
RUN chmod +rx /code/entry.sh
RUN cd code
ENV PATH="/code:$PATH"
ENV PORT=8050
EXPOSE 8050
ENTRYPOINT ["code/entry.sh"]