from flask import Flask, render_template, request, redirect, url_for
from models import db, Entry
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    entries = Entry.query.all()
    total_income = sum(entry.amount for entry in entries if entry.type == 'income')
    total_expense = sum(entry.amount for entry in entries if entry.type == 'expense')
    balance = total_income - total_expense
    return render_template('index.html', entries=entries, balance=balance)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        description = request.form['description']
        amount = float(request.form['amount'])
        entry_type = request.form['type']
        new_entry = Entry(date=date, description=description, amount=amount, type=entry_type)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_entry.html')

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('index'))    


if __name__ == '__main__':
    app.run(debug=True)
