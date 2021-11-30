from database import db
import datetime


class Post(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reply = db.relationship("Reply", backref="post", cascade="all, delete-orphan", lazy=True)
    report_total = db.Column("reported", db.Integer, default=0)
    views = db.Column("views", db.Integer, default=0)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    dislikes = db.relationship('PostDislike', backref='post', lazy='dynamic')

    def __init__(self, title, text, date, user_id, report_total, views):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = user_id
        self.report_total = report_total
        self.views = views


class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class PostDislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    posts = db.relationship("Post", backref="user", lazy=True)
    reply = db.relationship("Reply", backref="user", lazy=True)
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    disliked = db.relationship('PostDislike', foreign_keys='PostDislike.user_id', backref='user', lazy='dynamic')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

    def dislike_post(self, post):
        if not self.has_disliked_post(post):
            dislike = PostDislike(user_id=self.id, post_id=post.id)
            db.session.add(dislike)

    def undislike_post(self, post):
        if self.has_disliked_post(post):
            PostDislike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_disliked_post(self, post):
        return PostDislike.query.filter(PostDislike.user_id == self.id, PostDislike.post_id == post.id).count() > 0


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, post_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.post_id = post_id
        self.user_id = user_id

