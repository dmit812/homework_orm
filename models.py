import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), unique=True)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"))

    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), unique=True)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.NUMERIC(10, 2), nullable=False)
    date_sale = sq.Column(sq.Date, default=datetime.datetime.now)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
