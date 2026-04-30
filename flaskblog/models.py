from datetime import datetime
from flaskblog import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(100), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self): 
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800): # 1800s = 30m
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        # فقط لاظهار محتوى بشكل اكثر قابلية للقراءة بدون لا استطيع اظهار محتوى الإستعلام

    # +──────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
    # |  posts = db.relationship('Post', backref='author', lazy=True)                                                    |
    # |  |___> عرض معلومات صاحب المنشور بالكامل postخاصية عكسية وهي عبارة عن علاقة وليس عمود حقيقي, حتى أستطيع من جدول ال |
    # |  |___> user.posts وايضا الوصول الى المنشورات من داخل جدول المستخدم عن طريق استعلام post.author عن طريق استعلام     |
    # |                                                                                                                  |
    # |                                    User One ───────> Posts many                                                  |
    # |                                             <───────                                                             |
    # |                                              author                                                              |
    # +──────────────────────────────────────────────────────────────────────────────────────────────────────────────────+

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')" 




# +─────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
# |                  بعض التجارب على قاعدة البيانات وفهم العلاقة بين جدول المستخدمين والمنشورات                      |
# +─────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
  
# with app.app_context():

#     db.create_all()    

#     user_1 = User(username="Mohammed", email="M@gmail.com", password="M123M")
#     user_2 = User(username="Albasha", email="A@gmail.com", password="A123A")

#     # db.session.add(user_1)
#     # db.session.add(user_2)

#     print(User.query.all()) # [User('Mohammed', 'M@gmail.com', 'default.jpg'), User('Albasha', 'A@gmail.com', 'default.jpg')]
#     print(User.query.first()) # User('Mohammed', 'M@gmail.com', 'default.jpg')

#     # داخل الكلاس __rper__ شكل المخرج للإستعلام انا حددته في ال 

#     print(User.query.filter_by(username='Albasha').all()) # [User('Albasha', 'A@gmail.com', 'default.jpg')]
#     # |___> get يتعامل مع البيانات بمرونة اكثر من ال

#     print(User.query.get(2)) # User('Albasha', 'A@gmail.com', 'default.jpg')
#     # |___> id يتعامل مع المفتاح الأساسي رقم ال

#     user = User.query.filter_by(username='Mohammed').first()
#     print(user.id) # 1 >> من خلال استعلام معين, استطيع الوصول لاي عمود وعرض القيم الخاصة فيه Userمن خلال عمل انستنت من كلاس ال
#     print(user.posts) # [] ما في منشورات لهذا الشخص

#     post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id)
#     post_2 = Post(title='Blog 2', content='Second Post Content!', user_id=user.id)

#     # db.session.add(post_1)
#     # db.session.add(post_2)

#     print(user.posts) # [Post('Blog 1', '2026-04-18 04:05:21'), Post('Blog 2', '2026-04-18 04:05:21')]

#     for post in user.posts:
#         # print(post)
#         print(post.id, post.title, post.date_posted, post.user_id, sep=" | ")

#     # Output:
#     # 1 | Blog 1 | 2026-04-18 04:05:21 | 1
#     # 2 | Blog 2 | 2026-04-18 04:05:21 | 1


#     post = Post.query.first()
#     print(post) # Post('Blog 1', '2026-04-18 04:05:21') 
#     print(post.user_id) # 1
#     print(post.author) # User('Mohammed', 'M@gmail.com', 'default.jpg')

#     db.drop_all() # بمسح جميع الجداول الي انشاءتها سابفا مع البيانات
#     db.create_all() # يعيد انشاء الجداول
#     print(User.query.all()) # []
#     print(Post.query.all()) # []

#     db.session.commit() # مهم لحفظ التغيرات

# +─────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
