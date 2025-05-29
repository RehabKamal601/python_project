import psycopg2
from getpass import getpass

class LoanSystem:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="loan_system",
            user="rehab",
            password="12345",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def register(self):
        username = input("Enter new username: ")
        password = getpass("Enter password: ")
        try:
            self.cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
            print("Registration successful.")
        except Exception as e:
            self.conn.rollback()
            print("Error:", e)

    def login(self):
        username = input("Username: ")
        password = getpass("Password: ")
        self.cur.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = self.cur.fetchone()
        if user:
            print("Login successful!")
            return user[0]
        else:
            print("Invalid credentials.")
            return None

    def apply_for_loan(self, user_id):
        amount = float(input("Enter loan amount: "))
        self.cur.execute("INSERT INTO loans (user_id, amount) VALUES (%s, %s)", (user_id, amount))
        self.conn.commit()
        print("Loan application submitted.")

    def make_payment(self, user_id):
        self.cur.execute("SELECT l.id, l.amount - COALESCE(SUM(p.amount), 0) AS balance FROM loans l LEFT JOIN payments p ON l.id = p.loan_id WHERE l.user_id = %s GROUP BY l.id", (user_id,))
        loans = self.cur.fetchall()
        if not loans:
            print("No loans found.")
            return
        for loan in loans:
            print(f"Loan ID: {loan[0]}, Balance: {loan[1]}")
        loan_id = int(input("Enter Loan ID to pay: "))
        amount = float(input("Enter payment amount: "))
        self.cur.execute("INSERT INTO payments (loan_id, amount) VALUES (%s, %s)", (loan_id, amount))
        self.conn.commit()
        print("Payment successful.")

    def check_balance(self, user_id):
        self.cur.execute("""
            SELECT l.id, l.amount, COALESCE(SUM(p.amount), 0) as paid
            FROM loans l
            LEFT JOIN payments p ON l.id = p.loan_id
            WHERE l.user_id = %s
            GROUP BY l.id
        """, (user_id,))
        for loan_id, amount, paid in self.cur.fetchall():
            print(f"Loan ID: {loan_id}, Amount: {amount}, Paid: {paid}, Remaining: {amount - paid}")

    def view_history(self, user_id):
        self.cur.execute("""
            SELECT l.id, p.amount, p.payment_date
            FROM loans l
            JOIN payments p ON l.id = p.loan_id
            WHERE l.user_id = %s
            ORDER BY p.payment_date DESC
        """, (user_id,))
        for row in self.cur.fetchall():
            print(f"Loan ID: {row[0]}, Payment: {row[1]}, Date: {row[2]}")

    def close(self):
        self.cur.close()
        self.conn.close()

def main():
    app = LoanSystem()
    print("Welcome to Loan Application System")
    while True:
        choice = input("\n1. Register\n2. Login\n3. Exit\nChoose: ")
        if choice == "1":
            app.register()
        elif choice == "2":
            user_id = app.login()
            if user_id:
                while True:
                    option = input("\n1. Apply for Loan\n2. Make Payment\n3. Check Balance\n4. View History\n5. Logout\nChoose: ")
                    if option == "1":
                        app.apply_for_loan(user_id)
                    elif option == "2":
                        app.make_payment(user_id)
                    elif option == "3":
                        app.check_balance(user_id)
                    elif option == "4":
                        app.view_history(user_id)
                    elif option == "5":
                        break
        elif choice == "3":
            break
    app.close()

if __name__ == "__main__":
    main()
