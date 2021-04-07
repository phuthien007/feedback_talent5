from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime
from settings import *
from datetime import  datetime

class FeedBack(db.Model):
    __tablename__= 'feed_back'
    id= Column(Integer, primary_key=True)
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

if __name__=='__main__':
    db.create_all()