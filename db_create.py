# -*- coding: utf-8 -*-

from app.models import User, Party
from app import db

db.create_all()
db.session.commit()

admon = User('tomer', 'admon', '123456789', 0 ,0)
tomer = User(u'תומר', u'אדמון', '123456788', 0, 0)
alex = User('alex', 'shmukler', '314311770', 0, 0)
admin = User('a', 'a', '123', 0, 1)

avoda = Party(u'העבודה', 'https://www.am-1.org.il/wp-content/uploads/2015/03/%D7%94%D7%A2%D7%91%D7%95%D7%93%D7%94.-%D7%A6%D7%99%D7%9C%D7%95%D7%9D-%D7%99%D7%97%D7%A6.jpg', 0)
likud = Party(u'הליכוד', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Likud_Logo.svg/250px-Likud_Logo.svg.png', 0)
sass = Party(u'ש״ס', 'https://upload.wikimedia.org/wikipedia/he/thumb/0/05/Shas_logo.svg/150px-Shas_logo.svg.png', 0)
zioni = Party(u'מחנה הציוני', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/The_zionist_center.jpg/500px-The_zionist_center.jpg', 0)
atid = Party(u'יש עתיד', 'http://www.talschneider.com/wp-content/uploads/2012/04/%D7%9C%D7%95%D7%92%D7%95-%D7%99%D7%A9-%D7%A2%D7%AA%D7%99%D7%93.jpg', 0)
lavan = Party(u'פתק לבן', 'https://www.weberthai.com/fileadmin/user_upload/01_training-elements/02.4_others/02.5_color_cards/05_color_mosaic/images/1.jpg', 0)


db.session.add(sass)
db.session.add(zioni)
db.session.add(atid)
db.session.add(avoda)
db.session.add(likud)
db.session.add(lavan)
db.session.add(admon)
db.session.add(tomer)
db.session.add(alex)
db.session.commit()
users = User.query.all()
print users
