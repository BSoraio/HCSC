#根据数据库编写实体类
from . import db

#创建User类-user表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    uphone = db.Column(db.Integer,nullable=False)
    upwd = db.Column(db.String(30),nullable=False)
