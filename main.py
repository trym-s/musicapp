from db_connection import connect_to_db
from console_ui import * 

def main():
    """Programın ana döngüsü."""
    connection = connect_to_db()
    if not connection:
        print("Failed to connect to the database. Exiting.")
        return

    while True:
        display_options()
        try:
            option = int(input("Choose a query to execute: "))
            if option == 0:
                break
            process_option(option, connection)
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    connection.close()

if __name__ == "__main__":
    main()
