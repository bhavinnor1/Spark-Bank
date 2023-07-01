from flask import Flask, jsonify, render_template, request
import sqlite3 as sql

app=Flask(__name__)

@app.route('/')
def index():
	return render_template("home.html")

@app.route('/customers')
def view():
	with sql.connect("user_data.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM users;")
		rows = cur.fetchall()
	return render_template('customers.html',data=rows)

@app.route('/view', methods=['GET','POST'])
def transfer():
	sender=request.args.get('customer')
	with sql.connect("user_data.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM users;")
		rows = cur.fetchall()
		for i in range(0,len(rows)):
			if rows[i][0]==sender:
				rows.pop(i)
				break
		cur.execute(f'SELECT * FROM users WHERE Name="{sender}";')
		rows2 = cur.fetchall()
		cur.execute(f'SELECT * FROM transactions WHERE Sender="{sender}" OR Reciever="{sender}";')
		rows3 = cur.fetchall()
	return render_template('view.html',data=rows,name=sender,user_data=rows2,transactions=rows3[::-1])

@app.route('/transferto', methods=['GET','POST'])
def transferto():
	money=int(request.form['money'])
	sender=request.form['sender']
	reciever=request.form['reciever']
	with sql.connect("user_data.db") as con:
		cur = con.cursor()
		cur.execute(f'select Balance from users where Name="{reciever}"')
		rows=cur.fetchall()
		reciever_balance=rows[0][0]+money
		cur.execute(f'select Balance from users where Name="{sender}"')
		rows=cur.fetchall()
		sender_balance=rows[0][0]-money
		if rows[0][0]<money:
			msg='insufficient balance, transaction failed'
			cur.execute(f'insert into transactions values("{sender}","{reciever}",{money},"failed")')
			con.commit()
			con.rollback()
			return jsonify({'name' : 'error','obj': 'error','msg':msg})
		else:
			try:
				cur.execute(f'UPDATE users SET Balance = {sender_balance} WHERE Name="{sender}";')
				cur.execute(f'UPDATE users SET Balance = {reciever_balance} WHERE Name="{reciever}";')
			except Exception as e:
				con.rollback()
			con.commit()
			cur.execute(f'select Balance from users where Name="{reciever}"')
			rows=cur.fetchall()
			reciever_balance=rows[0][0]
			cur.execute(f'select Balance from users where Name="{sender}"')
			rows=cur.fetchall()
			sender_balance=rows[0][0]
		cur.execute(f'insert into transactions values("{sender}","{reciever}",{money},"success")')
		con.commit()
		cur.execute('select * from transactions;')
		rows=cur.fetchall()
	return jsonify({'sender' : sender, 'reciever':reciever,'obj': rows,'rb':reciever_balance,'sb':sender_balance})

@app.route('/transactions')
def transactions():
	with sql.connect("user_data.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM transactions;")
		rows = cur.fetchall()
	return render_template('transactions.html',data=rows[::-1])

if __name__=='__main__':
        app.run(host='0.0.0.0')
