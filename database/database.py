from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()



class Customer(Base):
    __tablename__ = 'customer'

    username = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    language = Column(String(250))
    phone = Column(String(250))
    location_keng = Column(String(250)) # latitude
    location_uzun = Column(String(250)) # longtitude
    ordered_products = relationship('Product', backref='customer', lazy='dynamic')


    @property
    def get_total_price(self):
        products = self.ordered_products
        total = 0
        for p in products:
            total += int(p.price)
        return total    
class Product(Base):
    __tablename__ = 'product'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    photo_id = Column(String(250)) 
    amount = Column(Integer) 
    price = Column(String(250))
    user_id = Column(Integer, ForeignKey('customer.id',ondelete='SET NULL'), nullable=True)

class Organization(Base):
    __tablename__ = 'organization'
    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    # address = Column(String(250)) 
    phone_number = Column(String(250)) 
    


engine = create_engine('postgresql://postgres:sindarov03@localhost:5432/postgres')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# # create a Session
session = Session()
# product = Product(title="Title", description=description, photo_id=file_id, amount=amount, price=price)
# session.add(product)
# # print(p.title)
# session.commit()

# organization = Organization(title="Markaz nomi", description="Biz sizga eng kerakli mahsulotlarni yetkazib beramiz.", phone_number="+123456789")
# session.add(organization)
# session.commit()
# print("commited")
# try :
#     customer = Customer(username="Murodbek", language="uz", phone="+998938727243",location_keng="40.344056", location_uzun="68.183421")
#     product = Product(title="something", description="some Description", amount=2, price=120, photo_id="afhuhfgaoghoagfg")
#     session.add(customer)
#     session.add(product)
#     session.commit()


#     p = session.query(Product).filter(Product.title == "something").first()
#     c= session.query(Customer).filter(Customer.username =="Asadbek").first()
#     if c and p:
#         c.ordered_products.append(p)
#         print(p.title + " added " + c.username + "'s product list")
#     c_list = c.ordered_products.all() # 1
#     for c in c_list:
#         print(c.title)
# except:
#     print("This username is already exists.")
# print(user.ordered_products.first().title) # <Address object at 0x10c098ed0>
# print(user.ordered_products.filter_by(title="something").count()) # 1
# del_product = user.ordered_products.filter_by(title="something").first()
# session.delete(del_product)
# session.commit()
# print(user.ordered_products.count()) # 1
# print(user.ordered_products.first()) # <Address object at 0x10c098ed0>
# print(user.ordered_products.filter_by(title="something").count()) # 1
