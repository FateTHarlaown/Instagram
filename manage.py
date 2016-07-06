
#-*- encoding=UTF-8 -*-

from Intasgraph import app, db
from flask_script import Manager
from sqlalchemy import or_, and_
from Intasgraph.models import User, Image, Comment
import random

manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('Rabbit' +str(i), 'a'+str(i)))
        for j in range(0, 10): #每人发十张图
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('Lover!~~Fucker~~!'+str(k), 1+10*i+j, i+1))
    db.session.commit()

    user = User.query.all()
    for u in user:
        print u
        for i in u.images:
            print i
            for c in i.comments:
                print c

if __name__ == '__main__':
    manager.run()
