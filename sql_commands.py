import cred
import psycopg2


def connection():  # Gets creds to connect to server
    conn = psycopg2.connect(database=cred.database,
                            host=cred.host,
                            user=cred.user,
                            password=cred.password,
                            port=cred.port)
    return conn


def add_items(file_name, item_name, price, date):
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO "Item_Listing" (item_name, price, date, group_name) VALUES (%s,%s,%s,%s);"""

    cursor.execute(query, (item_name, price, date, file_name))
    conn.commit()
    conn.close()


def add_links(item_name, link):
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO \"Links\" (item_name, link) VALUES (%s,%s);"""

    cursor.execute(query, (item_name, link))
    conn.commit()
    conn.close()


def get_data(name):
    conn = connection()
    cursor = conn.cursor()
    query = """A"""
# Retrieve data
# Detele a following
