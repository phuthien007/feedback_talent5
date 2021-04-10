from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, Boolean
from settings import *
from datetime import  datetime
from flask_login import UserMixin




class FeedBack(db.Model):
    __tablename__= 'feed_back'
    id= Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(200), nullable=False )
    course_name = Column(String(200), nullable=False)
    rating = Column(Integer)
    comments= Column(Text)
    create_date = Column(DateTime, default= datetime.utcnow())

    def __init__(self,  customer_name, course_name, rating, comments, create_data= datetime.now()):
        self.customer_name= customer_name
        self.course_name= course_name
        self.rating= rating
        self.comments=comments

class  User(db.Model, UserMixin):
    __tablename__= 'user'
    id= Column(Integer, primary_key=True, autoincrement=True)
    name= Column(String(100), nullable=False)
    active= Column(Boolean, default=True)
    username= Column(String(50), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    email= Column(String(100), nullable= False)
    def __init__(self,name, username, password, email):
        self.name=name
        self.username=username
        self.password=password
        self.email=email
    def __str__(self):
        return self.name


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()
if __name__ == '__main__':
    db.create_all()