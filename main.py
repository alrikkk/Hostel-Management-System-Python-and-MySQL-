import mysql.connector as mc

# Establish connection
con = mc.connect(host='localhost', user='root', password='KCS@TIGER', database='stdat')

if con.is_connected():
    print(" Connection successfully established")
else:
    print(" Connection failed!!")

# Create cursor
cur = con.cursor()

# Function to check if student exists
def check_student(admno):
    query = "SELECT COUNT(*) FROM STUDENTS WHERE admno = {}".format(admno)
    cur.execute(query)
    count = cur.fetchone()[0]
    return count > 0

while True:
    print("\n----- HOSTEL MANAGEMENT SYSTEM -----")
    print("1. Add a Student")
    print("2. Delete a Student")
    print("3. Display Student Details")
    print("4. Update Student Details")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ")
    
    # ---------------- ADD STUDENT ----------------
    if choice == '1':
        n = int(input("Enter number of students to add: "))
        for i in range(n):
            name = input("Enter name: ")
            stu_class = input("Enter class: ")
            dob = input("Enter DOB (DD/MM/YYYY): ")
            admno = input("Enter admission number: ")
            gender = input("Enter gender (M/F): ")
            address = input("Enter address: ")
            
            if check_student(admno):
                print("Admission number already exists! Try again.")
                continue
                
            query = ("INSERT INTO STUDENTS (name, class, dob, admno, gender, address) "
                     "VALUES ('{}', '{}', '{}', {}, '{}', '{}')"
                     .format(name, stu_class, dob, admno, gender, address))
            cur.execute(query)
            con.commit()
            print("Student added successfully!")
            
    # ---------------- DELETE STUDENT ----------------
    elif choice == '2':
        admno = input("Enter admission number to delete: ")
        if not check_student(admno):
            print("No such student found!")
        else:
            query = "DELETE FROM STUDENTS WHERE admno = {}".format(admno)
            cur.execute(query)
            con.commit()
            print("Student deleted successfully!")
            
    # ---------------- DISPLAY STUDENT ----------------
    elif choice == '3':
        admno = input("Enter admission number to display: ")
        if not check_student(admno):
            print("No student found!")
        else:
            query = "SELECT * FROM STUDENTS WHERE admno = {}".format(admno)
            cur.execute(query)
            record = cur.fetchone()
            print("\n--- Student Details ---")
            print("Name:", record[1])
            print("Class:", record[2])
            print("DOB:", record[3])
            print("Admission No:", record[4])
            print("Gender:", record[5])
            print("Address:", record[6])
            
    # ---------------- UPDATE STUDENT ----------------
    elif choice == '4':
        admno = input("Enter admission number to update: ")
        if not check_student(admno):
            print("No student found!")
            continue
            
        print("\nWhat do you want to update?")
        print("1. Name")
        print("2. Class")
        print("3. DOB")
        print("4. Gender")
        print("5. Address")
        
        update_choice = input("Enter choice (1-5): ")
        fields = {'1': 'name', '2': 'class', '3': 'dob', '4': 'gender', '5': 'address'}
        
        if update_choice not in fields:
            print("Invalid choice!")
            continue
            
        new_value = input(f"Enter new {fields[update_choice]}: ")
        query = "UPDATE STUDENTS SET {} = '{}' WHERE admno = {}".format(fields[update_choice], new_value, admno)
        cur.execute(query)
        con.commit()
        print(f"{fields[update_choice].capitalize()} updated successfully!")
        
    # ---------------- EXIT ----------------
    elif choice == '5':
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice! Please try again.")

# Close connection
cur.close()
con.close()
