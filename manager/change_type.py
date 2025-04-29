from starter import *
import os
import json

products = CRUD.for_model(Product).all(db_session)
# print(products, len(products))
for product in products:
    print(type(product.photo), product.photo)
    # print(json.dumps([product.photo]))
    # CRUD.for_model(Product).update(db_session, product.id, photo=json.dumps([product.photo]))