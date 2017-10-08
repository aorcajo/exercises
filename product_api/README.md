# Porducts API

### Getting Started

Install the requirements (virtual env is recommended):

```
pip3 install -r requirements.txt
```

### Preparing the DB

```
python3 app.py db init
python3 app.py db migrate
python3 app.py db upgrade
```

### Load initial data
```
python3 load_csv.py import_data *path_to_csv_file*
```

### Running


```
python3 app.py runserver
```

The api will be accesible by default from http://127.0.0.1:5000/product
