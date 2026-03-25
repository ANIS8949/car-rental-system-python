import pyodbc

conn=pyodbc.connect(
    'Driver={SQL Server};'
    'SERVER=FAIJAN\MSSQL;'
    'DATABASE=CarRentalDB;'
    'Trusted_connection=yes;'
)

cursor=conn.cursor()





class Car:
    
    def __init__(self, car_id, brand, model, year):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.year = year
        self.is_available = True

    def display(self):
        status = "Available" if self.is_available else "Rented"
        print(f"ID: {self.car_id} | {self.brand} {self.model} ({self.year}) | {status}")


class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.rented_cars = []

    def display(self):
        print(f"Customer ID: {self.customer_id} | Name: {self.name}")


class CarRentalSystem:
    def __init__(self):
        self.cars = {}
        self.customers = {}

    def add_car(self):
        car_id = int(input("Enter car ID: "))
        brand = input("Enter Brand: ").capitalize()
        model = input("Enter Model: ").capitalize()
        year = int(input("Enter Year: "))

       

        cursor.execute(
            "Insert into cars values(?,?,?,?,?)",
            (car_id,brand,model,year,1)
        )
        conn.commit()

        print("Car Added Successfully.")

    def add_customer(self):
        customer_id = int(input("Enter Customer ID: "))
        name = input("Enter Customer Name: ").capitalize()

        

        cursor.execute(
            "Insert into customers values(?,?)",
            (customer_id,name)
        )
        conn.commit()

        print("Customer added successfully.")

    
    def display_available_cars(self):

            cursor.execute("SELECT * FROM Cars WHERE is_available=1")

            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"ID:{row.car_id} | {row.brand} {row.model} ({row.year}) | Available")
            else:
                print("No cars available.")

    def rent_car(self):

        car_id = int(input("Enter Car ID: "))
        customer_id = int(input("Enter Customer ID: "))

        cursor.execute("SELECT is_available FROM Cars WHERE car_id=?", (car_id,))
        car = cursor.fetchone()

        if car and car.is_available:

            cursor.execute(
                "UPDATE Cars SET is_available=0 WHERE car_id=?",
                (car_id,)
             )

            cursor.execute(
                "INSERT INTO Rentals(car_id,customer_id,status) VALUES (?,?,?)",
                (car_id,customer_id,"Rented")
             )

            conn.commit()

            print("Car rented successfully.")

        else:
            print("Car not available.")

    def return_car(self):

        car_id = int(input("Enter Car ID: "))

        cursor.execute(
            "UPDATE Cars SET is_available=1 WHERE car_id=?",
            (car_id,)
         )

        cursor.execute(
            "UPDATE Rentals SET status='Returned' WHERE car_id=?",
            (car_id,)
        )

        conn.commit()

    print("Car returned successfully.")

    def display_customer_rentals(self):

        customer_id = int(input("Enter Customer ID: "))

        cursor.execute("""
            SELECT Cars.car_id, Cars.brand, Cars.model, Cars.year
            FROM Rentals
            JOIN Cars ON Rentals.car_id = Cars.car_id
            WHERE Rentals.customer_id=? AND Rentals.status='Rented'
            """,(customer_id,))

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(f"ID:{row.car_id} | {row.brand} {row.model} ({row.year})")
        else:
            print("No cars rented.")
    def display_rental_history(self):

        cursor.execute("""
        SELECT Rentals.rental_id,
        Customers.name,
        Cars.brand,
        Cars.model,
        Cars.year,
        Rentals.status
        FROM Rentals
        JOIN Cars ON Rentals.car_id = Cars.car_id
        JOIN Customers ON Rentals.customer_id = Customers.customer_id
        """)

        rows = cursor.fetchall()

        if rows:
            print("\n------ Rental History ------")
            for row in rows:
                print(f"Rental ID:{row.rental_id} | Customer:{row.name} | "
                  f"Car:{row.brand} {row.model} ({row.year}) | Status:{row.status}")
        else:
            print("No rental history found.")

system = CarRentalSystem()

while True:
    print("\n--------- Car Rental System ---------")
    print("1. Add Car")
    print("2. Add Customer")
    print("3. Display Available Cars")
    print("4. Rent Car")
    print("5. Return Car")
    print("6. Display Customer Rentals")
    print("7. Exit")

    choice = int(input("Enter Your Choice: "))

    if choice == 1:
        system.add_car()

    elif choice == 2:
        system.add_customer()

    elif choice == 3:
        system.display_available_cars()

    elif choice == 4:
        system.rent_car()

    elif choice == 5:
        system.return_car()

    elif choice == 6:
        system.display_customer_rentals()

    elif choice == 7:
        system.display_rental_history()

    elif choice == 8:
        print("Thank you for using the system.")
        break
        

    else:
        print("Invalid choice! Try again.")