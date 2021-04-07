from models import *


# get data
def get_data_rating():
    with db.engine.begin() as conn:
        rows= conn.execute('SELECT course_name ,count(rating) FROM feed_back group by  rating,course_name').fetchall()
        return rows
def get_data_comments():
    with db.engine.begin() as conn:
        rows= conn.execute('SELECT course_name ,count(comments) FROM feed_back where comments is not null group by course_name ').fetchall()
        return rows

def get_data_comments_by_date():
    with db.engine.begin() as conn:
        rows= conn.execute("SELECT create_date::timestamp::date date ,count(comments) FROM feed_back group by  (create_date::timestamp::date )").fetchall()
        return rows
def get_each_element_rating():
    with db.engine.begin() as conn:
        rows= conn.execute("SELECT rating FROM feed_back").fetchall()
        return rows