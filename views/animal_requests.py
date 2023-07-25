import sqlite3
from models import Animal, Location, Customer

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "status": "Admitted",
        "breed": "Chihuahua",
        "customer_id": 4,
        "locationId": 1

    },
    {
        "id": 2,
        "name": "Roman",
        "status": "Admitted",
        "breed": "Dalmatian",
        "customer_id": 2,
        "locationId": 1
    },
    {
        "id": 3,
        "name": "Blue",
        "status": "Admitted",
        "breed": "Russian Blue",
        "customer_id": 1,
        "locationId": 2
    },
    {
        "id": 4,
        "name": "Eleanor",
        "status": "Admitted",
        "breed": "Italian Greyhound",
        "customerId": 2,
        "locationId": 1
    }
]


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.email customer_email,
            c.address customer_address,
            c.password customer_password
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['status'], row['breed'],
                            row['customer_id'], row['location_id'])

            # Create a Location instance from the current row
            location = Location(
                row['id'], row['location_name'], row['location_address'])

            # Create a Customer instance from the current row
            customer = Customer(
                row['id'], row['customer_name'], row['customer_email'], row['customer_address'], row['customer_password'])

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            # Add the dictionary representation of the customer to the animal
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return animals


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
        FROM animal a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'], data['status'],
                        data['customer_id'], data['location_id'],
                        )

        return animal.__dict__


def get_animal_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
        FROM animal a
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'], row['name'], row['status'], row['breed'], row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return animals


def get_animal_by_status(status):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
        FROM animal a
        WHERE a.status = ?
        """, (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'], row['name'], row['status'], row['breed'], row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return animals


def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with `id` property added
    return animal


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                status = ?,
                breed = ?,
                customer_id = ?,
                location_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['status'], new_animal['breed'],
              new_animal['customer_id'],
              new_animal['location_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
