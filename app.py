from mailbox import Mailbox, Message
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify ,session
import json
import smtplib

app = Flask(__name__)
app.secret_key = 'AVVIGNESSH9347317236@#$%^&*()'

with open('books.json', 'r') as f:
    books = json.load(f)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email_address@gmail.com'
SMTP_PASSWORD = 'your_email_password'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            query = request.form.get('query', '').lower()
            results = []
            if query:
                for book in books:
                    if query in book['title'].lower() or query in book['author'].lower():
                        results.append(book)
                if not results:
                    flash(f"No books found for '{query}'. Please send a request to add this book.", 'info')
                    return redirect(url_for('add_book', title=query))
            else:
                results = books
            return render_template('index.html', books=results, query=query)
        return render_template('index.html', books=books)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with open('users.json', 'r') as f:
            users = json.load(f)
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('index'))
        error = 'Invalid username or password'
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        with open('users.json', 'r') as f:
            users = json.load(f)
        for user in users:
            if user['username'] == username:
                error = 'Username already exists'
                return render_template('signup.html', error=error)
        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)
        new_user = {'username': username, 'password': password}
        users.append(new_user)
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' in session:
        if request.method == 'POST':
            # Get form data for title and author only
            title = request.form['title']
            author = request.form['author']
            
            # Fixed values for description, copies, and image
            description = "A tragic love story set against the backdrop of the Roaring Twenties."
            copies = 3
            image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqFwZQbGEIbHiafLlSQBybdGjNSToF9IRdm-XcSg63&s"
            
            # Create a new book dictionary with fixed description, copies, and image
            new_book = {
                'title': title,
                'author': author,
                'description': description,
                'copies': copies,
                'image': image
            }
            
            # Load existing books, add the new book, and save to books.json
            with open('books.json', 'r') as f:
                books = json.load(f)
            books.append(new_book)
            with open('books.json', 'w') as f:
                json.dump(books, f, indent=4)
            
            flash('Your book has been added successfully.', 'success')
            return redirect(url_for('index'))
        return render_template('add_book.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)


