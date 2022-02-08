from flask import *
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login', methods=["GET","POST"])
def login():
	name=request.form['name']
	ip=request.remote_addr
	ua=request.user_agent.string
	k=name+'$'+ip+'$'+ua
	res=f.encrypt(k.encode()).decode()
	resp = make_response(redirect('/dashboard'))
	resp.set_cookie('id', res, max_age=3600)
	return resp 
	
@app.route('/dashboard')
def dashboard():
	id=request.cookies.get('id')
	if id==None:
		return render_template('notloggedin.html')
	k=f.decrypt(id.encode()).decode()
	arr=k.split('$')
	name=arr[0]
	ip=arr[1]
	ua=arr[2]
	if ip==request.remote_addr and ua==request.user_agent.string:
		return render_template('dashboard.html',name=name, ip=ip, ua=ua)
	else:
		return render_template('error.html', ip1=ip, ua1=ua, ip2=request.remote_addr, ua2=request.user_agent.string)
	
app.run(host='0.0.0.0', port=5000)
