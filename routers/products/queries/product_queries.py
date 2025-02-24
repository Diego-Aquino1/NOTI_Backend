from operator import or_
from sqlmodel import Session, select, func

from models.product import Product

class ProductQuery:
    def __init__(self, session: Session):
        self.db = session

    def find_all(self):
        query = select(Product)

        return self.db.exec(query).all()