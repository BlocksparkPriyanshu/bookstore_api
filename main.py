import mysql.connector as mysql

db = mysql.connect(
    host = "192.168.0.111",
    user = "root",
    passwd = "admin"
)


from flask import Flask
from flask import jsonify 
from flask import request
app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({'message': 'Please required fill the details'}), 400
    username=data['username']
    password=data['password']
    email=data['email']

    cursor = db.cursor()
    insert_query="""INSERT INTO user.user_table(username,password,email) VALUES(%s,%s,%s)"""
    cursor.execute(insert_query,(username,password,email))
    db.commit()

    if len(username)< 3 or len(password)<3:
        return jsonify({'message': 'Invalid Input'}), 409
    
    
    return jsonify({'message': 'User registered successfully'})
    


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username=data.get('username')
    password=data.get('password')

    cursor =db.cursor()
    select_query="SELECT * FROM user.user_table WHERE username = %s AND password = %s"
    cursor.execute(select_query,(username,password))
    user=cursor.fetchone()
    db.commit()

    if user:
        return jsonify("Login Successfully")
    else:
        return jsonify("Please enter correct username or password")
    
    


@app.route('/api/books', methods=['GET'])
def books():
     cursor = db.cursor()
     cursor.execute("SELECT * FROM user.book_table") 
     book_table = cursor.fetchall()
     
    
     return jsonify(book_table),201



@app.route('/api/add_books', methods=['POST'])
def add_books():
    
    new_book = request.get_json()

    title=new_book['title']
    author=new_book['author']
    price=new_book['price']
    quantity_available=new_book['quantity_available']

    cursor = db.cursor()
    insert_query="""INSERT INTO user.book_table(title, author, price, quantity_available) VALUES(%s,%s,%s,%s)"""
    cursor.execute(insert_query,(title, author, price, quantity_available))
    db.commit()
    return jsonify("Successful Added Book"), 201

@app.route('/api/books/<book_id>', methods=['GET'])
def book(book_id):
    cursor = db.cursor()
    
    query ="SELECT * FROM user.book_table WHERE id =%s"
    cursor.execute(query,(book_id,))
    book_table = cursor.fetchone()
    
    return jsonify(book_table)

@app.route('/api/books/<book_id>', methods=['PUT'])
def books_update(book_id):
    cursor = db.cursor()
    data = request.get_json()
    new_title = data.get('title')
    new_author = data.get('author')
    new_price = data.get('price')
    new_quantity_available = data.get('quantity_available')
    
    if not new_title and not new_author and not new_price and not new_quantity_available:
        return jsonify("No Data Provided For Update")
    
    try:
        if new_title:
            cursor.execute("UPDATE user.book_table SET title =%s WHERE id =%s ",(new_title, book_id))
        if new_author:
            cursor.execute("UPDATE user.book_table SET author =%s WHERE id =%s ",(new_author, book_id))
        if new_price:
            cursor.execute("UPDATE user.book_table SET price =%s WHERE id =%s ",(new_price, book_id))
        if new_quantity_available:
            cursor.execute("UPDATE user.book_table SET quantity_available =%s WHERE id =%s ",(new_quantity_available, book_id))
        db.commit()
        return jsonify("Successfully Data Upadated")
    except:
        return jsonify("error")
    
@app.route('/books/<book_id>', methods=['DELETE'], endpoint='delete_book')
def books_delete(book_id):
    cursor=db.cursor()
    delete_query= "DELETE FROM user.book_table WHERE id=%s"

    cursor.execute(delete_query,(book_id,))
    db.commit()
    return jsonify("Data Deleted Successfull")
    
    

@app.route('/api/cart', methods=['POST'])
def add_cart():
    cart_data=request.get_json()

    user_id=cart_data['user_id']
    book_id=cart_data['book_id']
    quantity=cart_data['quantity']


    
    cursor=db.cursor()
    insert_query="""INSERT INTO user.cart_table(user_id,book_id,quantity) VALUES(%s,%s,%s)"""
    cursor.execute(insert_query,(user_id,book_id,quantity))
    db.commit()
    return jsonify("Successfully book added into the shopping cart")

@app.route('/api/cart', methods=['PUT'])
def update():
    cart_data=request.get_json()
    new_quantity=cart_data['quantity']
    new_user_id=cart_data['user_id']
    new_book_id=cart_data['book_id']

    cursor=db.cursor()

    if not  new_quantity :
        return jsonify("No Data Provided For Update")
    
    if new_quantity:
        cursor.execute("UPDATE user.cart_table SET quantity =%s WHERE user_id = %s AND book_id = %s ",(new_quantity,new_user_id ,new_book_id))
        db.commit()
    return jsonify("Successfully added quantity of book")

@app.route('/api/cart', methods=['GET'])
def user_content():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user.cart_table") 
    cart_table = cursor.fetchall()
    
    return jsonify(cart_table) 

@app.route('/api/cart/',methods=['DELETE'], endpoint="delete_cart_book")
def delete_book(book_id):
    cursor = db.cursor()
    delete_query=("DELETE FROM user.cart_table WHERE id=%s")

   
    cursor.execute(delete_query,(book_id,))
    db.commit()
    return jsonify("Book Deleted Successfully")

@app.route('/api/orders/', methods=['POST'])
def new_order():
    new_book = request.get_json()
    book_id=new_book['book_id']
    user_id=new_book['user_id']
    total_price=new_book['total_price']
    status=new_book['status']

    cursor=db.cursor()
    insert_query="""INSERT INTO user.order_table(user_id,book_id,total_price,status) VALUES(%s,%s,%s,%s)"""
    cursor.execute(insert_query,(user_id,book_id, total_price,status))
    db.commit()
    return jsonify("Successfully new order place")

@app.route('/api/orders/', methods = ['GET'])
def all_orders():
    cursor=db.cursor()
    cursor.execute("SELECT * FROM user.order_table")
    order_table=cursor.fetchall()
    return jsonify(order_table)   

if __name__ == '__main__':
    app.run(debug=True) 