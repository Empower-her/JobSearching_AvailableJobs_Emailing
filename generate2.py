import sqlite3
import random
import string

# Database connection
def get_db_connection():
    conn = sqlite3.connect('job_portal2.db')  # SQLite database file
    return conn

# Create user and job tables if they do not exist
def create_tables(conn):
    # Create User Table
    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emailid TEXT UNIQUE,
            name TEXT,
            skill1 TEXT,
            skill2 TEXT,
            skill3 TEXT,
            password TEXT
        )
    """)

    # Create Job Tables
    job_types = [
        'housekeeper', 'homecook', 'beautician',
        'caretaker', 'hostel_cook', 'laundry',
        'nanny', 'playschool_teacher', 'shop_attendant'
    ]

    for job_type in job_types:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {job_type} (
                jobid INTEGER PRIMARY KEY AUTOINCREMENT,
                name_of_organization TEXT,
                phone_number TEXT,
                location TEXT,
                salary INTEGER,
                emailid TEXT  -- New column added
            )
        """)

    conn.commit()

# Function to add a user
def add_user(conn, emailid, name, skill1, skill2, skill3, password):
    try:
        conn.execute("""
            INSERT INTO user (emailid, name, skill1, skill2, skill3, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (emailid, name, skill1, skill2, skill3, password))
        conn.commit()
        print("User added successfully.")
    except sqlite3.IntegrityError:
        print("User with this email already exists.")

# Function to update user details
def update_user(conn, user_id, name=None, skill1=None, skill2=None, skill3=None):
    fields = []
    values = []
    
    if name:
        fields.append("name = ?")
        values.append(name)
    if skill1:
        fields.append("skill1 = ?")
        values.append(skill1)
    if skill2:
        fields.append("skill2 = ?")
        values.append(skill2)
    if skill3:
        fields.append("skill3 = ?")
        values.append(skill3)
    
    if fields:
        query = f"UPDATE user SET {', '.join(fields)} WHERE user_id = ?"
        values.append(user_id)
        conn.execute(query, values)
        conn.commit()
        print("User updated successfully.")
    else:
        print("No fields to update.")

# Function to delete a user
def delete_user(conn, user_id):
    conn.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
    conn.commit()
    print("User deleted successfully.")

# Function to add a job
def add_job(conn, job_type, name_of_organization, phone_number, location, salary, emailid):
    conn.execute(f"""
        INSERT INTO {job_type} (name_of_organization, phone_number, location, salary, emailid)
        VALUES (?, ?, ?, ?, ?)
    """, (name_of_organization, phone_number, location, salary, emailid))
    conn.commit()
    print("Job added successfully.")

# Function to update job details
def update_job(conn, job_type, jobid, name_of_organization=None, phone_number=None, location=None, salary=None):
    fields = []
    values = []
    
    if name_of_organization:
        fields.append("name_of_organization = ?")
        values.append(name_of_organization)
    if phone_number:
        fields.append("phone_number = ?")
        values.append(phone_number)
    if location:
        fields.append("location = ?")
        values.append(location)
    if salary:
        fields.append("salary = ?")
        values.append(salary)
    
    if fields:
        query = f"UPDATE {job_type} SET {', '.join(fields)} WHERE jobid = ?"
        values.append(jobid)
        conn.execute(query, values)
        conn.commit()
        print("Job updated successfully.")
    else:
        print("No fields to update.")

# Function to delete a job
def delete_job(conn, job_type, jobid):
    conn.execute(f"DELETE FROM {job_type} WHERE jobid = ?", (jobid,))
    conn.commit()
    print("Job deleted successfully.")

# Main Menu Function
def main_menu():
    conn = get_db_connection()
    create_tables(conn)

    while True:
        print("\n--- Job Portal Database Management ---")
        print("1. Add User")
        print("2. Update User")
        print("3. Delete User")
        print("4. Add Job")
        print("5. Update Job")
        print("6. Delete Job")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            emailid = input("Enter emailid: ")
            name = input("Enter name: ")
            skill1 = input("Enter skill1: ")
            skill2 = input("Enter skill2: ")
            skill3 = input("Enter skill3: ")
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            add_user(conn, emailid, name, skill1, skill2, skill3, password)

        elif choice == '2':
            user_id = int(input("Enter user_id to update: "))
            name = input("Enter new name (leave blank to skip): ") or None
            skill1 = input("Enter new skill1 (leave blank to skip): ") or None
            skill2 = input("Enter new skill2 (leave blank to skip): ") or None
            skill3 = input("Enter new skill3 (leave blank to skip): ") or None
            update_user(conn, user_id, name, skill1, skill2, skill3)

        elif choice == '3':
            user_id = int(input("Enter user_id to delete: "))
            delete_user(conn, user_id)

        elif choice == '4':
            job_type = input("Enter job type: ")
            name_of_organization = input("Enter name of organization: ")
            phone_number = input("Enter phone number: ")
            location = input("Enter location: ")
            salary = int(input("Enter salary: "))
            emailid = input("Enter user emailid (to associate with job): ")
            add_job(conn, job_type, name_of_organization, phone_number, location, salary, emailid)

        elif choice == '5':
            job_type = input("Enter job type: ")
            jobid = int(input("Enter jobid to update: "))
            name_of_organization = input("Enter new name of organization (leave blank to skip): ") or None
            phone_number = input("Enter new phone number (leave blank to skip): ") or None
            location = input("Enter new location (leave blank to skip): ") or None
            salary = input("Enter new salary (leave blank to skip): ")
            salary = int(salary) if salary else None
            update_job(conn, job_type, jobid, name_of_organization, phone_number, location, salary)

        elif choice == '6':
            job_type = input("Enter job type: ")
            jobid = int(input("Enter jobid to delete: "))
            delete_job(conn, job_type, jobid)

        elif choice == '7':
            break

        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == '__main__':
    main_menu()
