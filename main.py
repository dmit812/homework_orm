import sqlalchemy
from sqlalchemy.orm import sessionmaker

import json

from models import create_tables, Publisher, Shop, Book, Stock, Sale

if __name__ == '__main__':

    DSN = 'postgresql://postgres:postgres@localhost:5432/netology_db'
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json', 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    q = input('Введите имя автора: ')
    for qf in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale, Sale.count).\
        join(Publisher).join(Stock).join(Shop).join(Sale).\
            filter(Publisher.name == q):
        print(f'{qf.title.ljust(40)} | {qf.name.ljust(10)} | '
              f'{str(qf.price * qf.count).ljust(10)} | {qf.date_sale}')

    session.close()
