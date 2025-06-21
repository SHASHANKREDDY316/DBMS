from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Database connection config
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'showroom'

def get_db():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# ---------- Cars ----------
@app.route('/api/cars', methods=['GET', 'POST'])
def cars_api():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM cars")
        rows = cursor.fetchall()
        db.close()
        return jsonify(rows)
    data = request.get_json()
    sql = "INSERT INTO cars (Model, Year, Price, Color, Stock) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (data['Model'], data['Year'], data['Price'], data['Color'], data['Stock']))
    car_id = cursor.lastrowid
    db.close()
    return jsonify({"CarID": car_id, **data}), 201

@app.route('/api/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM cars WHERE CarID=%s", (id,))
    db.close()
    return '', 204

@app.route('/api/cars/search', methods=['GET'])
def search_cars():
    model = request.args.get('model', '')
    color = request.args.get('color', '')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cars WHERE Model LIKE %s OR Color LIKE %s", (f"%{model}%", f"%{color}%"))
    rows = cursor.fetchall()
    db.close()
    return jsonify(rows)

# ---------- Customers ----------
@app.route('/api/customers', methods=['GET', 'POST'])
def customers_api():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        db.close()
        return jsonify(rows)
    data = request.get_json()
    sql = "INSERT INTO customers (Name, Email, Phone, Address) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data['Name'], data['Email'], data.get('Phone'), data.get('Address')))
    customer_id = cursor.lastrowid
    db.close()
    return jsonify({"CustomerID": customer_id, **data}), 201

@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM customers WHERE CustomerID=%s", (id,))
    db.close()
    return '', 204

# ---------- Employees ----------
@app.route('/api/employees', methods=['GET', 'POST'])
def employees_api():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        db.close()
        return jsonify(rows)
    data = request.get_json()
    sql = "INSERT INTO employees (Name, Role, Email, Phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data['Name'], data['Role'], data.get('Email'), data.get('Phone')))
    emp_id = cursor.lastrowid
    db.close()
    return jsonify({"EmployeeID": emp_id, **data}), 201

@app.route('/api/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM employees WHERE EmployeeID=%s", (id,))
    db.close()
    return '', 204

# ---------- Services ----------
@app.route('/api/services', methods=['GET', 'POST'])
def services_api():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM services")
        rows = cursor.fetchall()
        db.close()
        return jsonify(rows)
    data = request.get_json()
    sql = "INSERT INTO services (CarID, CustomerID, ServiceDate, Description, Cost) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (data['CarID'], data['CustomerID'], data['ServiceDate'], data['Description'], data['Cost']))
    service_id = cursor.lastrowid
    db.close()
    return jsonify({"ServiceID": service_id, **data}), 201

@app.route('/api/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM services WHERE ServiceID=%s", (id,))
    db.close()
    return '', 204

# ---------- Payments ----------
@app.route('/api/payments', methods=['GET', 'POST'])
def payments_api():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM payments")
        rows = cursor.fetchall()
        db.close()
        return jsonify(rows)
    data = request.get_json()
    sql = "INSERT INTO payments (CustomerID, Amount, Date, Method) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data['CustomerID'], data['Amount'], data['Date'], data['Method']))
    payment_id = cursor.lastrowid
    db.close()
    return jsonify({"PaymentID": payment_id, **data}), 201

@app.route('/api/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM payments WHERE PaymentID=%s", (id,))
    db.close()
    return '', 204

# ---------- Sales ----------
@app.route('/api/sales', methods=['GET', 'POST'])
def sales_api():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        db.close()
        return jsonify(rows)
    # POST
    data = request.get_json()
    sql = """
    INSERT INTO sales (CarID, CustomerID, DrivingLicense, Amount, Price, Date, Method, PaymentType)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
        sql,
        (
            data['CarID'],
            data['CustomerID'],
            data.get('DrivingLicense'),
            data.get('Amount'),
            data.get('Price'),
            data.get('Date'),
            data.get('Method'),
            data.get('PaymentType')
        )
    )
    sale_id = cursor.lastrowid

    # Optionally decrement car stock after sale
    cursor.execute("UPDATE cars SET Stock = Stock - 1 WHERE CarID = %s", (data['CarID'],))

    db.close()
    return jsonify({"SaleID": sale_id, **data}), 201

@app.route('/api/sales/<int:id>', methods=['DELETE'])
def delete_sale(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM sales WHERE SaleID=%s", (id,))
    db.close()
    return '', 204

@app.route('/api/sales/search', methods=['GET'])
def search_sales():
    customer_id = request.args.get('customer_id')
    car_id = request.args.get('car_id')
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM sales WHERE 1=1"
    params = []
    if customer_id:
        query += " AND CustomerID = %s"
        params.append(customer_id)
    if car_id:
        query += " AND CarID = %s"
        params.append(car_id)
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    db.close()
    return jsonify(rows)

# ---------- User Signup & Login ----------
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    if not (fullname and email and password and phone):
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    db = get_db()
    cursor = db.cursor()
    # Check for existing email or phone
    cursor.execute("SELECT * FROM users WHERE Email=%s OR Phone=%s", (email, phone))
    if cursor.fetchone():
        db.close()
        return jsonify({'success': False, 'message': 'Email or phone already registered.'}), 409

    pw_hash = generate_password_hash(password)
    cursor.execute("INSERT INTO users (FullName, Email, Phone, PasswordHash) VALUES (%s, %s, %s, %s)",
                   (fullname, email, phone, pw_hash))
    db.close()
    return jsonify({'success': True})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    if not (phone and password):
        return jsonify({'success': False, 'message': 'Phone and password required.'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE Phone=%s", (phone,))
    user = cursor.fetchone()
    db.close()
    if user and check_password_hash(user['PasswordHash'], password):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid phone or password.'}), 401

if __name__ == '__main__':
    app.run(debug=True)