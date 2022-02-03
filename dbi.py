import mariadb as db
import dbcreds

# Creating a function to connect to database, assigning None to conn and cursor before try-except block and then returning conn and cursor when the connection is established


def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=dbcreds.user, password=dbcreds.password,
                          host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except:
        print("Something went wrong!")
    return conn, cursor

# Creating a function to disconnect from database, closing connection for conn and cursor


def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except:
        print("The issue with cursor")
    try:
        conn.close()
    except:
        print("The issue with connection")

# This function is created for user authentication.


def attempt_login(username, password):
    # Assigning a variable to None before using it in try-except block
    user = None
    # This is what is returned by connect_db()
    conn, cursor = connect_db()
# Trying to execute a select query for user to make sure their username(alias) and password match to the ones in db
    try:
        cursor.execute(
            "select id from hackers h where alias= ? and password= ?", [username, password])
        user = cursor.fetchone()
# Handling errors
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
# Using this function to disconnect from db and passing arguments returned by connect_db()
    disconnect_db(conn, cursor)
# Returning values for cursor.fetchone()
    if(user == None):
        return False, None
    else:
        # If there is a match in the db, user_id is also returned. This way we can add new things and list the existing ones based on the user's ownership.
        return True, user[0]

# This function will add a new exploit based on the user_id(the user who added the exploit)


def add_exploit(exploit_input, user_id):
    # This was commented above
    conn, cursor = connect_db()
    try:
        # Trying to add(insert) new value in db under the user who is logged in
        cursor.execute(
            "insert into exploits(content, user_id) values(?, ?)", [
                exploit_input, user_id]
        )
        # Saving changes
        conn.commit()
        # Handling errors
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
# This was commented above
    disconnect_db(conn, cursor)

# This function allows to see all the exploits created by the user who's logged in


def list_your_exploits(user_id):
    # Assigning a variable to None before using it in try-except block
    exploits = None
    conn, cursor = connect_db()
    try:
        # Select statement which prints all table columns based on the user_id (the user who added those exploits)
        cursor.execute(
            "select id, content, user_id from exploits where user_id =?", [user_id])
        print("Here are the available exploits:")
        # Fetching all rows from the db
        exploits = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    for exploit in exploits:
        print("")
        # Printing values from a tuple
        print(f"Id: {exploit[0]} Content: {exploit[1]} User: {exploit[2]}")
        print("")

# This function allows to see all the exploits created by other users and not by the one who is logged in


def list_other_exploits(user_id):
    # Assigning a variable to None before using it in try-except block
    exploits = None
    conn, cursor = connect_db()
    try:
        # Select statement which prints all exploits from other users (not the one who is logged in)
        cursor.execute(
            "select id, content, user_id from exploits where user_id !=?", [user_id])
        print("Here are the available exploits:")
        exploits = cursor.fetchall()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB query, please file bug report")
    except:
        print("Something went wrong!")
    disconnect_db(conn, cursor)
    for exploit in exploits:
        print("")
        # Printing values from a tuple
        print(f"Id: {exploit[0]} Content: {exploit[1]} User: {exploit[2]}")
        print("")
