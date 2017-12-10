from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), index=True, unique=False)
    last_name = db.Column(db.String(120), index=True, unique=False)
    id_num = db.Column(db.String(9), index=True, unique=True)
    isVoted = db.Column(db.Integer)
    role = db.Column(db.Integer)

    def __init__(self, first_name, last_name, id_num, isvoted, role):
        self.first_name = first_name
        self.last_name = last_name
        self.id_num = id_num
        self.isVoted = isvoted
        self.role = role

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.first_name


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    picture = db.Column(db.String(120), index=True, unique=False)
    sum = db.Column(db.Integer)

    def __init__(self, name, picture, summ):
        self.name = name
        self.picture = picture
        self.sum = summ

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<Party %r>' % self.name
