import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
LOCALHOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')


BOOKS = "product_id, product_name, product_price, product_finalprice, product_url, image_src, discount"

# Check product exists
def check_product(product_id):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        cursor = conn.cursor()

        # execute the select statement
        cursor.execute("SELECT product_id FROM product WHERE product_id = %s", (product_id,))

        # fetch the record
        record = cursor.fetchone()

        # check if the record exists
        if record is not None:
            return True
        else:
            return False

    except mysql.connector.Error as error:
        print("Failed to check record into MySQL table: {}".format(error))
        return False

def insert_data(data):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        cursor = conn.cursor()

        # Prepare the SQL statement
        if check_product(data["product_id"]):
            return False
        
        if (data.get("type_id") == "series"):
            return False

        sql = "INSERT INTO product (" + BOOKS + ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (
            data.get("product_id"),
            data.get("product_name"),
            data.get("product_price"),
            data.get("product_finalprice"),
            data.get("product_url"),
            data.get("image_src"),
            data.get("discount")
        )
        # execute the select statement
        cursor.execute(sql, val)

        # Commit the changes to the database
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))
        return False

def edit_product(product_id, data):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        cursor = conn.cursor()

        # Prepare the SQL statement
        if check_product(data["product_id"]):
            return False
        
        # prepare the SQL query
        sql = "UPDATE product SET product_id=%s, product_name=%s, product_price=%s, \
            product_finalprice=%s, product_url=%s, image_src=%s, discount=%s"

        # extract the values from the data dictionary
        val = (
            data.get("product_id"),
            data.get("product_name"),
            data.get("product_price"),
            data.get("product_finalprice"),
            data.get("product_url"),
            data.get("image_src"),
            data.get("discount")
        )
        # execute the SQL query with the values
        cursor.execute(sql, val)

        # commit the changes to the database
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))
        return False


def remove_product(product_id):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        # create a cursor object
        cursor = conn.cursor()
        if not check_product(product_id):
            return False
        # prepare the SQL query
        sql_query = "DELETE FROM product WHERE product_id = %s"

        # execute the SQL query with the product_id parameter
        cursor.execute(sql_query, (product_id,))

        # commit the changes to the database
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))
        return False
if __name__ == '__main__':
    pass

    
    