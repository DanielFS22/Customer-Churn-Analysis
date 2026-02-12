import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="janeiro2002",
        database="churn_project"
    )
    return connection

if __name__ == "__main__":
    conn = create_connection()
    print("Conexão realizada com sucesso!")
    conn.close()
