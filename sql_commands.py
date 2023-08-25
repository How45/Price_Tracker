import cred
import psycopg2


def connection():  # Gets creds to connect to server
    conn = psycopg2.connect(database=cred.database,
                            host=cred.host,
                            user=cred.user,
                            password=cred.password,
                            port=cred.port)
    return conn


def add_following(follow_name):
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO "Following" (group_name) VALUES (%s)"""

    cursor.execute(query, follow_name)  # Pending transaction
    conn.commit()  # Commit transaction
    conn.close()


def add_items(follow_name, item_name, price, date):
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO "Item_Listing" (item_name, price, date, group_name) VALUES (%s,%f,%s,%s)"""

    cursor.execute(query, (follow_name, item_name, date, price))
    conn.commit()
    conn.close()


def add_links(item_names, link):
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO "Links" (item_name, link) VALUES (%s,%s)"""

    cursor.execute(query, (item_names, link))
    conn.commit()
    conn.close()

# Detele a following
