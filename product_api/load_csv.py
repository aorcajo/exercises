import csv
from datetime import datetime

from flask_script import Manager

from app import app, db, Product


manager = Manager(app)

BULK_SIZE = 500


def commit_data(session, bulk):
    session.bulk_save_objects(bulk)

    try:
        session.commit()
    except:
        session.rollback()


@manager.command
def import_data(csv_filename):

    with open(csv_filename, 'r') as csvfile:
        datareader = csv.DictReader(csvfile)

        bulk = []

        for row in datareader:
            row['id'] = int(row[''])
            del row['']
            try:
                row['timestamp'] = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                row['timestamp'] = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')

            bulk.append(Product(**row))

            if len(bulk) >= BULK_SIZE:
                commit_data(db.session, bulk)
                bulk = []

        if bulk:
            commit_data(db.session, bulk)


@manager.command
def delete_data():
    db.engine.execute(Product.__table__.delete())
    print(len(Product.query.all()))


if __name__ == "__main__":
    manager.run()
