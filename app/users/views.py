#处理与用户业务逻辑相关的视图和路由
from . import users
from ..import db
from ..models import *
from flask import render_template, request, session, redirect, make_response

@users.route('/')
def index():
  return "hello"

@users.route('/login',methods=['GET','POST'])
def login_views():
  if request.method == 'GET':
    # 获取请求原地址,并保存在session中
    url = request.headers.get('Referer', '/')
    session['url'] = url
    # 判断session有没有uname
    if 'uphone' in session:
      return redirect(url)
    else:
      # session中没有uname的值,继续判断cookie
      if 'uphone' in request.cookies:
        # cookies中有uname,从cookie中获取uname的值
        uphone = request.cookies['uphone']
        # 判断uname的有效性(值是否为admin,可以判断DB)
        uphone_db = User.query.filter_by(uphone=uphone)
        if uphone == uphone_db:
          # 用户名正确,将uname保存进session
          session['uphone'] = uphone
          return redirect(url)
        else:
          # 用户名不正确
          resp = make_response(
            render_template('login.html')
          )
          # 通过resp删除cookies中uname的值
          resp.delete_cookie('uphone')
          return resp
      else:
        # 没有uname
        return render_template('login.html')
  else:
    #接收前端传递过来的用户名和密码
    uphone = request.form['uphone']
    upwd = request.form['password']
    #查询数据库,验证用户名和密码是否存在
    user=User.query.filter_by(uphone=uphone,upwd=upwd).first()
    #根据结果保存进session
    if user:
      # 登录成功后的处理
      # 1.将登录名称保存进session
      session['uphone'] = uphone
      # 2.从session中将url获取出来,构建响应对象
      url = session['url']
      resp = redirect(url)
      # 3.判断是否要记住密码,记住密码则将uname保存进cookie
      if 'isSaved' in request.form:
        resp.set_cookie('uphone', uphone, 60 * 60 * 24 * 365 * 10)
      return resp
    else:
      # 登录失败的处理
      return render_template('login.html')


@users.route('/register',methods=['GET','POST'])
def register_views():
  if request.method == 'GET':
    return render_template('register.html')
  else:
    uphone = request.form['uphone']
    upwd = request.form['upwd']


