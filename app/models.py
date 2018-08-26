from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://flask:flask@127.0.0.1:3306/movieweb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

# 用户信息
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)    # 用户名
    pwd = db.Column(db.String(100))                  # 用户密码
    email = db.Column(db.String(50), unique=True)   # 用户邮箱
    phone = db.Column(db.String(11), unique=True)   # 用户手机号码
    info = db.Column(db.Text)                       # 用户简介
    face = db.Column(db.String(255), unique=True)   # 用户头像
    createtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 用户创建时间
    uuid = db.Column(db.String(255), unique=True)   # 唯一id
    userlogs = db.relationship('Userlog', backref='user') #会员日志关系外键
    comments = db.relationship('Comment', backref='user') #电影评论关系外键
    moviecols = db.relationship('Moviecol', backref='user') #电影收藏关系外键

    def __repr__(self):
        return '<User %r>' % self.name

# 用户日志
class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(50))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Userlog %r>' % self.id

# 电影标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    movies = db.relationship('Movie', backref='tag') # 电影外键关联

    def __repr__(self):
        return '<Tag %r>' % self.name

# 电影详细信息
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True) # 标题
    url = db.Column(db.String(255), unique=True)   # 地址
    info = db.Column(db.Text)                      # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    start = db.Column(db.SmallInteger)             # 星级
    playnum = db.Column(db.BigInteger)             # 播放量
    conmmentnum = db.Column(db.BigInteger)         # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id')) # 所属标签
    area = db.Column(db.String(255))               # 上映地区
    releasetime = db.Column(db.Date)               # 上映时间
    length = db.Column(db.String(100))             # 电影时长
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    comments = db.relationship('Comment', backref='movie') #电影评论关系外键
    moviecols = db.relationship('Moviecol', backref='movie') #电影收藏关系外键


    def __repr__(self):
        return "<Movie %r>" % self.title

# 电影预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title

# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)    # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Comment %r>" % self.id

# 电影收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Moviecol %r>" % self.id

# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Auth %r>" % self.name

# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return "<Auth %r>" % self.name

# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)    # 用户名
    pwd = db.Column(db.String(100))                  # 用户密码
    is_super = db.Column(db.SmallInteger)           # 是否为超级管理员，0表示为超级管理员
    role_id = db.Column(db.Integer, db.FetchedValue('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 添加时间
    adminlogs = db.relationship('Adminlog', backref='admin')    # 管理员登录日志外键
    adminlogs = db.relationship('Oplog', backref='admin')    # 操作日志外键

    def __repr__(self):
        return '<Admin %r>' % self.name

# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(50))   # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Adminlog %r>' % self.id

# 操作日志
class Oplog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(50))   # 登录ip
    reason = db.Column(db.String(600)) # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Oplog %r>' % self.id

if __name__ == '__main__':
    db.create_all()