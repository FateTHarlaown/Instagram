from flask_script import Manager
from Intasgraph import app
from Intasgraph import db
from Intasgraph.models import user, address


manager = Manager(app)


@manager.command
def tuser():
    print 'now to create database'
    db.drop_all()
    db.create_all()
    for i in range(1, 10):
        db.session.add(user('coder'+str(i), 'password'+str(i)))
    db.session.commit()
    for i in range(1, 10):
        db.session.add(address(i, 'hell'+str(i)))
    db.session.commit()
    for i in range(1, 10):
        u = user.query.filter_by(id=i).first()
        print u, u.address.first()


if __name__ == '__main__':
    manager.run()
