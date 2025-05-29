# Loan Application System (Terminal-Based)

This is a simple terminal-based Loan Application System developed in Python. It uses PostgreSQL as the backend database and helps users to apply for loans, make payments, check balances, and view payment history.

## 📌 Features

- User registration and login
- Apply for a loan
- Make partial or full payments
- Check loan balance
- View payment history
- Uses PostgreSQL for data persistence
- Secure password handling using `getpass`

## ⚙️ Technologies Used

- Python 3
- PostgreSQL
- psycopg2 library
- DBeaver (for database management)

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/RehabKamal601/python_project.git
   cd python_project
   ```

2. **Install dependencies**
   ```bash
   sudo apt install python3-pip
   pip3 install psycopg2-binary
   ```

3. **Set up the PostgreSQL database**
   - Create a database: `loan_system`
   - Create tables using `loan_system_tables.sql` or DBeaver.

4. **Run the project**
   ```bash
   python3 main.py
   ```

## 📂 Database Tables

- `users`: Stores user login info.
- `loans`: Stores loan details for each user.
- `payments`: Stores payment history.

## 🙋‍♀️ Author

- Rehab Kamal

---

✅ Contributions and suggestions are welcome!
