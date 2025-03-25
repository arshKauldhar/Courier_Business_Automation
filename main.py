import os
import oracledb
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DB_USER = os.getenv("ORACLE_USER")
DB_PASSWORD = os.getenv("ORACLE_PASSWORD")
DB_DSN = os.getenv("ORACLE_DSN")
SECRET_KEY = os.getenv("SECRET_KEY")

# Database connection
connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
cursor = connection.cursor()

# Flask app configuration
app = Flask(__name__, template_folder='templates')
app.secret_key = SECRET_KEY
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/login_submit', methods=['POST'])
def login_submit():
    role = request.form.get('role')
    username = request.form.get('username')
    password = request.form.get('pwd')

    # Validate user credentials
    cursor.execute(
        "SELECT * FROM project_data.person WHERE P_role = :role AND Phone_no = :username AND P_password = :password", 
        {'role': role, 'username': username, 'password': password}
    )
    user = cursor.fetchone()

    if user:
        session['username'] = username
        session['role'] = role
        session['logged_in'] = True

        if role == "admin":
            return redirect(url_for('admin_page'))
        elif role == "employee":
            return redirect(url_for('employee_page'))
        else:
            cursor.execute("SELECT P_name FROM project_data.person WHERE phone_no = :1", (username,))
            P_name = cursor.fetchone()[0]
            session['P_name'] = P_name
            return redirect(url_for('user_page'))
    else:
        error_msg = "Incorrect username or password. Please try again."
        return render_template('login.html', error_msg=error_msg)

@app.route('/admin')
def admin_page():
    if 'logged_in' in session and session['role'] == 'admin':
        return render_template('admin.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/employee')
def employee_page():
    if 'logged_in' in session and session['role'] == 'employee':
        return render_template('employee.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/user')
def user_page():
    if 'logged_in' in session and session['role'] not in ['admin', 'employee']:
        return render_template('user.html', P_name=session['P_name'], username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/keep-alive')
def keep_alive():
    session.modified = True
    return '', 204


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/tracking')
def tracking():
    return render_template('tracking.html')

@app.route('/contact')
def contact_us():
    try:
        return render_template('contact.html')
    except Exception as e:
        print('Error rendering contact us page:', e)
        return jsonify({'error': 'Server error'}), 500

@app.route('/submit_account_form', methods=['POST'])
def submit_account_form():
    try:
        phone = request.form['phone']
        # Check if the user already exists
        cursor.execute("SELECT COUNT(*) FROM person WHERE Phone_no = :1", (phone,))
        connection.commit()
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            return "User with this phone number already exists. Please choose a different phone number."
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        city = request.form['city']
        
        
        # Insert data into the "person" table
        cursor.execute("""
            INSERT INTO person (Phone_no, P_password, P_name, Age, Area_or_village, city)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, (phone, password, name, age, address, city))
        connection.commit()

        return "Account created successfully"
    
    except Exception as e:
        # Handle any exceptions that occur during execution
        return f"An error occurred: {str(e)}"

# see user details on a user page 
@app.route('/account_profile')
def account_profile():
    username = session.get('username')
    
    # Check if the username is available in the session
    if username:
        cursor.execute("SELECT phone_no, P_password, P_name, age, area_or_village, city FROM project_data.person WHERE phone_no = :username", {'username': username})
        user_details = cursor.fetchone()  
        if user_details:
            return render_template('user_details.html', user_details=user_details)
        else:
            return "User details not found."
    else:
        return redirect(url_for('login'))

# to change a password from a user page 
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        username = session.get('username')

        if username:
            # Fetch the user's current password from the database
            cursor.execute("SELECT P_password FROM project_data.person WHERE phone_no = :username", {'username': username})
            user_password = cursor.fetchone()[0]

            if user_password == old_password:
                if new_password == confirm_password:
                    # Update the user's password in the database
                    cursor.execute("UPDATE project_data.person SET P_password = :new_password WHERE phone_no = :username", {'new_password': new_password, 'username': username})
                    connection.commit()
                    return "Password changed successfully."
                else:
                    return "New password and confirmation do not match."
            else:
                return "Old password is incorrect."
        else:
            return redirect(url_for('login'))
    return render_template('change_password.html')

@app.route('/user/add_order_details', methods=['POST'])
def add_order_details():
    try:
        R_phone_no = request.form['R_phone']
        recipient_name = request.form['recipient_name']
        R_address = request.form['address']
        city= request.form['R_City']
        sender_id = request.form['sender-id']
        pick_up_address = request.form['pick_up_address']
        pick_up_city = request.form['pick_up_city']
        preferred_delivery_date = request.form['preferred_delivery_date']
        discription = request.form['order_description']
        order_weight = request.form['order_weight']
        distance = request.form['distance']
        amount = request.form['totalBill']
        payment_mode = request.form['mode']
        
        # Check if recipient exists
        cursor.execute("SELECT * FROM project_data.recipient WHERE R_phone = :1", {"1": R_phone_no})
        recipient_found = cursor.fetchall()

        if recipient_found:
            # Update recipient if it exists
            cursor.execute("""
                UPDATE project_data.recipient 
                SET R_name = :1, area_or_village = :2, city = :3
                WHERE R_phone = :4
                """, (recipient_name, R_address, city, R_phone_no))
        else:
            # Insert recipient if it doesn't exist
            cursor.execute("""
                INSERT INTO project_data.recipient (R_phone, R_name, area_or_village, city)
                VALUES (:1, :2, :3, :4)
                """, (R_phone_no, recipient_name, R_address, city))

        # Generate a UUID
        generated_bill_id = str(uuid.uuid4())
        bill_id = generated_bill_id[:10] 

        # Insert data into the bill table with the generated bill ID
        cursor.execute("""
            INSERT INTO project_data.bill (Bill_Id, Amount, B_Mode, Cus_id)
            VALUES (:1, :2, :3, :4)""",
            (bill_id, amount, payment_mode, sender_id))

        # Commit the transaction to make the changes permanent
        connection.commit()      
          
        # Insert data into Order_Tracking table
        tracking_id = f"TRK_{bill_id}"  # Generate a tracking ID based on bill ID
        cursor.execute("""INSERT INTO project_data.Order_Tracking(Tracking_id, Start_location, Current_status, Destination_location)
                       VALUES (:1, :2, 'Ready for Pick Up', :3)""",
                       (tracking_id, pick_up_address, city)) 

        # Insert data into courier_order table
        cursor.execute("""INSERT INTO project_data.Courier_Order(Pick_up_address,pick_up_city, Preffered_delivery_date, Order_weight, 
                       O_Bill_id, O_tracking_id, start_location,
                       Sender_id, Recipient_id, distance, discription) 
                       VALUES (:1,:2,TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6, :7, :8, :9, :10, :11)
                       """, 
                       (pick_up_address,pick_up_city, preferred_delivery_date, order_weight, bill_id,tracking_id,pick_up_address, sender_id,R_phone_no,distance,discription) )
        
        connection.commit()
        
        cursor.execute("""SELECT co.Order_Id, co.O_tracking_id, co.Expected_delivery_date, b.Amount AS total_order_price,
                        r.R_name AS recipient_name, r.R_phone AS recipient_contact, r.area_or_village || ', ' || r.city AS recipient_address
                        FROM project_data.Courier_Order co
                        JOIN project_data.recipient r ON co.Recipient_id = r.R_phone
                        JOIN project_data.bill b ON co.O_Bill_id = b.Bill_Id
                        WHERE co.Sender_id = :sender_id 
                        ORDER BY co.Order_Date DESC  
                        FETCH FIRST 1 ROW ONLY""", {"sender_id": sender_id}) 

        order_details = cursor.fetchone() # Fetch the result from the cursor

        # Pass fetched data to the template for rendering
        return render_template('orderplaced.html',
                            order_id=order_details[0],
                            tracking_id=order_details[1],
                            expected_delivery_date=order_details[2],
                            total_order_price=order_details[3],
                            recipient_name=order_details[4],
                            recipient_contact=order_details[5],
                            recipient_address=order_details[6])
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)
        connection.rollback()  # Rollback transaction in case of error
        return jsonify({'error': 'Error occurred while inserting data'})
   
@app.route('/admin/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        try:
            phone = request.form['phone']
            password = request.form['password']
            name = request.form['name']
            age = request.form['age']
            address = request.form['address']
            city = request.form['city']
            role = request.form['role']
            designation = request.form.get('designation')
            join_date = request.form.get('join_date')
            e_branch_id = request.form.get('e_branch_id')
            
            # Insert data into the "person" table
            cursor.execute("""
                INSERT INTO project_data.person (Phone_no, P_password, P_name, Age, Area_or_village, city, P_role)
                VALUES (:1, :2, :3, :4, :5, :6, :7)
            """, (phone, password, name, age, address, city, role))
            connection.commit()

            # Execute SQL query
            sql = "INSERT INTO project_data.employee (emp_user_id, designation, join_date,e_branch_id) VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4)"
            cursor.execute(sql, (phone, designation, join_date,e_branch_id))
            connection.commit()

            return "Employee added successfully"

        except Exception as e:
            connection.rollback()
            print("Error:", e)
            return "An error occurred while adding the employee"

@app.route('/admin/update_employee', methods=['POST'])
def update_employee():
    emp_user_id = request.form['emp_user_id']
    new_address = request.form['new_address']
    new_city = request.form['new_city']
    e_branch_id = request.form.get('e_branch_id')

    try:
        # Update the employee information
        cursor.execute("""
            UPDATE project_data.person
            SET area_or_village = :1, city = :2
            WHERE phone_no = :3
        """, (new_address, new_city, emp_user_id))
        connection.commit()
        
        cursor.execute("""
            UPDATE project_data.employee
            SET e_branch_id = :1
            WHERE emp_user_id = :2
        """, (e_branch_id,emp_user_id))
        connection.commit()

        return "Employee information updated successfully"
    except Exception as e:
        connection.rollback()
        print("Error:", e)
        return "An error occurred while updating the employee information"

@app.route('/admin/delete_employee', methods=['POST'])
def delete_employee():
    emp_user_id = request.form['emp_user_id']

    try:
        # Delete the employee from the employee table
        cursor.execute("DELETE FROM project_data.employee WHERE emp_user_id = :1", (emp_user_id,))
        connection.commit()

        # Also delete the employee from the person table
        cursor.execute("DELETE FROM project_data.person WHERE phone_no = :1", (emp_user_id,))
        connection.commit()

        return jsonify({'message': 'Employee deleted successfully'}), 200

    except oracledb.Error as e:
        return jsonify({'error': f'An error occurred while deleting the employee: {e}'}), 500

@app.route('/admin/display_employee', methods=['GET'])
def display_employee():
    cursor.execute("""SELECT e.emp_user_id, e.designation, e.join_date,
                    p.P_name, p.age, p.area_or_village, p.city, p.P_role
                    FROM project_data.employee e
                    JOIN project_data.person p ON e.emp_user_id = p.phone_no
                    """)
    employees = cursor.fetchall()

    # Convert the fetched data into a list of dictionaries
    employee_data = [
        {
            "emp_user_id": row[0],
            "designation": row[1],
            "join_date": row[2],
            "P_name": row[3],
            "age": row[4],
            "area_or_village": row[5],
            "city": row[6],
            "P_role": row[7]
        }
        for row in employees
    ]
    return jsonify(employee_data)

@app.route('/admin/add_branch', methods=['POST'])
def create_branch():
    if request.method == 'POST':
        try:
            # Extract data from the form
            branch_id = request.form.get('branch_id')
            city = request.form.get('city')
            address = request.form.get('address')
            contact = request.form.get('contact')
            manager_id = request.form.get('manager_id')

            # Execute SQL query
            sql = """INSERT INTO project_data.branch (branch_id, city, address, B_phone, manager_id) 
                     VALUES (:1, :2, :3, :4, :5)"""
            cursor.execute(sql, (branch_id, city, address, contact, manager_id))
            connection.commit()

            # Return a valid response
            return "Details added successfully"

        except Exception as e:
            # Rollback in case of any error
            connection.rollback()
            print("Error:", e)
            # You might want to handle the error appropriately, like displaying an error message
            return "An error occurred while adding details"
        
    else:
        return "Invalid request method"
    
@app.route('/admin/update_branch', methods=['POST'])
def update_branch():
    if request.method == 'POST':
        try:
            # Extract data from the form
            branch_id = request.form.get('branch_id')
            city = request.form.get('city')
            address = request.form.get('address')
            contact = request.form.get('contact')
            manager_id = request.form.get('manager_id')

            # Execute SQL query for update
            sql = """UPDATE project_data.branch 
                     SET city = :city, address = :address, B_phone = :contact, manager_id = :manager_id 
                     WHERE branch_id = :branch_id"""
            cursor.execute(sql, {'city': city, 'address': address, 'contact': contact, 'manager_id': manager_id, 'branch_id': branch_id})
            connection.commit()

            # Return a valid response
            return "Branch details updated successfully"

        except Exception as e:
            # Rollback in case of any error
            connection.rollback()
            print("Error:", e)
            # You might want to handle the error appropriately, like displaying an error message
            return "An error occurred while updating branch details"
        
    else:
        return "Invalid request method"

@app.route('/admin/delete_branch', methods=['POST'])
def delete_branch():
    if request.method == 'POST':
        try:
            # Extract data from the form
            branch_id = request.form.get('branch_id')

            # Execute SQL query for deletion
            sql = "DELETE FROM project_data.branch WHERE branch_id = :branch_id"
            cursor.execute(sql, {'branch_id': branch_id})
            connection.commit()

            # Return a valid response
            return "Branch deleted successfully"

        except Exception as e:
            # Rollback in case of any error
            connection.rollback()
            print("Error:", e)
            # You might want to handle the error appropriately, like displaying an error message
            return "An error occurred while deleting the branch"

    else:
        return "Invalid request method"

@app.route('/admin/get_branches', methods=['GET'])
def get_branches():
    cursor.execute("SELECT * FROM project_data.branch")
    branches = cursor.fetchall()
    return jsonify(branches)

# Route to add a pickup employee for an order
@app.route('/admin/add_pickup_emp', methods=['POST'])
def add_pickup_employee():
    if request.method == 'POST':
        try:
            # Extract data from the form
            order_id = request.form.get('order_id')
            pick_emp_id = request.form.get('pick_emp_id')

            # Execute SQL query to update the order with the pickup employee ID
            sql = """UPDATE project_data.Courier_Order 
                     SET Pick_emp_id = :pick_emp_id 
                     WHERE Order_Id = :order_id"""
            cursor.execute(sql, {'pick_emp_id': pick_emp_id, 'order_id': order_id})
            connection.commit()

            # Return a success message
            return "Pickup employee added successfully to the order"

        except Exception as e:
            connection.rollback()
            print("Error:", e)
            return "An error occurred while adding pickup employee to the order"
    else:
        return "Invalid request method"

# Route to add a delivery employee for an order
@app.route('/admin/add_delivery_emp', methods=['POST'])
def add_delivery_employee():
    if request.method == 'POST':
        try:
            # Extract data from the form
            order_id = request.form.get('order_id')
            delivery_emp_id = request.form.get('delivery_emp_id')

            # Execute SQL query to update the order with the delivery employee ID
            sql = """UPDATE project_data.Courier_Order 
                     SET Delivery_emp_id = :delivery_emp_id 
                     WHERE Order_Id = :order_id"""
            cursor.execute(sql, {'delivery_emp_id': delivery_emp_id, 'order_id': order_id})
            connection.commit()

            # Return a success message
            return "Delivery employee added successfully to the order"

        except Exception as e:
            connection.rollback()
            print("Error:", e)
            return "An error occurred while adding delivery employee to the order"
    else:
        return "Invalid request method"

@app.route('/admin/get_orders', methods=['GET'])
def get_orders():
    try:
        # Execute SQL query to fetch order data
        cursor.execute("""
            SELECT Order_Id, Order_Date, Pick_emp_id, Delivery_emp_id, Sender_id, Recipient_id
            FROM project_data.Courier_Order
            ORDER BY Order_Date ASC
        """)
        orders = cursor.fetchall()

        # Return orders as JSON response
        return jsonify(orders)

    except Exception as e:
        print("Error:", e)
        return jsonify([])  # Return empty list if an error occurs

@app.route('/employee/view_orders', methods=['GET'])
def view_orders():
    try:
        # Execute SQL query to fetch order data
        cursor.execute("""SELECT  Order_Id,Order_Date,Pick_up_address,Actual_delivery_date,Order_weight,Pick_emp_id,
                       Delivery_emp_id,O_Bill_id ,O_tracking_id,start_location,Sender_id,Recipient_id
                       FROM project_data.Courier_Order""")
        orders = cursor.fetchall()

        # Return orders as JSON response
        return jsonify(orders)

    except Exception as e:
        print("Error:", e)
        return jsonify([])  # Return empty list if an error occurs

@app.route('/update_actual_delivery', methods=['POST'])
def update_actual_delivery():
    try:
        data = request.json
        
        # Extract order ID and new actual delivery date from the data
        order_id = data['orderId']
        new_actual_delivery = data['newActualDelivery']
        
        cursor.execute("""
                        UPDATE project_data.Courier_Order
                        SET Actual_delivery_date = TO_DATE(:new_actual_delivery, 'YYYY-MM-DD')
                        WHERE Order_Id = :order_id""",
                        {'new_actual_delivery': new_actual_delivery, 'order_id': order_id})
                            
        # Commit changes to the database
        connection.commit()
        
        # Return a success response
        return "Actual delivery date updated successfully"

    except Exception as e:
        print("Error:", e)
        connection.rollback()
        return "An error occurred while updating actual delivery date"

@app.route('/get_tracking', methods=['GET'])
def get_tracking():
    tracking_id = request.args.get('trackingId')

    # Fetch data from the database
    cursor.execute("SELECT * FROM Order_Tracking WHERE Tracking_id=:1", (tracking_id,))
    rows = cursor.fetchall()

    # Process fetched data
    result = []
    for row in rows:
        result.append({
            "Tracking_id": row[0],
            "Start_location": row[1],
            "Pickup_time": str(row[2]),
            "Current_status": row[3],
            "Destination_location": row[4],
            "Received_time": str(row[5])
        })

    return jsonify(result)
     
@app.route('/update_tracking', methods=['POST'])
def update_tracking():
    data = request.json
    tracking_id = data['trackingId']
    pickup_time = data['pickupTime']
    status = data['status']
    received_time = data['receivedTime']
    receiver_name = data['receiverName']
    receiver_relation = data['receiverRelation']

    try:
        # Update the tracking data in Oracle database
        cursor.execute("""
            UPDATE Order_Tracking 
            SET Pickup_time = TO_DATE(:pickup_time, 'YYYY-MM-DD"T"HH24:MI'), 
                Current_status = :status, 
                Received_time = TO_DATE(:received_time, 'YYYY-MM-DD"T"HH24:MI')
            WHERE Tracking_id = :tracking_id
        """, {'pickup_time': pickup_time, 'status': status, 'received_time': received_time, 'tracking_id': tracking_id})

        # Update the recipient table
        cursor.execute("""
            UPDATE recipient
            SET receiver_name = :receiver_name,
                receiver_rel_with_recipient = :receiver_relation
            WHERE R_phone = (SELECT Recipient_id FROM Courier_Order WHERE O_tracking_id = :tracking_id)
        """, {'receiver_name': receiver_name, 'receiver_relation': receiver_relation, 'tracking_id': tracking_id})

        # Commit the transaction
        connection.commit()

        return jsonify({"message": "Tracking information and recipient details updated successfully."})

    except oracledb.Error as error:
        print("Error updating tracking information:", error)
        return jsonify({"message": "An error occurred while updating tracking information."})

def get_user_orders(user_id):
    query = """
    SELECT
        Order_ID, Order_Date, Recipient_id, bill.Amount AS Price,
        Order_Tracking.Current_status AS Status, Tracking_id AS Tracking_Id
    FROM project_data.Courier_Order
    LEFT JOIN project_data.bill ON project_data.Courier_Order.O_Bill_id = project_data.bill.Bill_Id
    LEFT JOIN project_data.Order_Tracking ON project_data.Courier_Order.O_tracking_id = project_data.Order_Tracking.Tracking_id
    WHERE Sender_id = :user_id
    ORDER BY Order_Date ASC
    """
    cursor.execute(query, user_id=user_id)
    orders = cursor.fetchall()
    return orders

@app.route('/orders')
def orders():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session['username']
    orders = get_user_orders(user_id)
    return render_template('viewOrders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)