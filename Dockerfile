FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY ./product_api /app

RUN pip install -r /app/requirements.txt
RUN python /app/app.py db init
RUN python /app/app.py db migrate
RUN python /app/app.py db upgrade

COPY products.csv /
RUN python /app/load_csv.py import_data /products.csv
RUN rm /products.csv

