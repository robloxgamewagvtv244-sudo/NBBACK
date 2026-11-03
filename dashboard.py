import os
from flask import Flask,request,session,redirect
from dotenv import load_dotenv
load_dotenv(); app=Flask(__name__); app.secret_key=os.getenv('DASH_SECRET','change-me')
PW=os.getenv('DASH_PASSWORD','')
@app.route('/',methods=['GET','POST'])
def home():
 if request.method=='POST':
  if not PW or request.form.get('password')!=PW: return 'Sai mật khẩu hoặc chưa đặt DASH_PASSWORD',401
  session['ok']=True; return redirect('/')
 if not session.get('ok'):
  return '<meta name="viewport" content="width=device-width"><h1>NBBACK Dashboard</h1><form method="post"><input name="password" type="password" placeholder="Mật khẩu"><button>Đăng nhập</button></form>'
 return '<meta name="viewport" content="width=device-width"><h1>⚡ NBBACK Dashboard</h1><p>Bot: Moderation · Ticket · XP · Music · Games · Logs · Giveaway</p><p>Tiến trình bot chạy riêng bằng python bot.py.</p><a href="/logout">Đăng xuất</a>'
@app.route('/logout')
def logout(): session.clear(); return redirect('/')
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','8080')))
