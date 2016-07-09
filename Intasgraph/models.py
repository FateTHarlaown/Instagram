from Intasgraph import db


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)
    address = db.relationship('address', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User:%s ID:%d Password:%s>' % (self.username, self.id, self.password)


class address(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addr = db.Column(db.String(255), primary_key=True)

    def __init__(self, person_id, addr):
        self.person_id = person_id
        self.addr = addr

    def __repr__(self):
        return '<user_id: %d address: %s>' % (self.person_id, self.addr)
