import cred
import psycopg2


def connection():  # Gets creds to connect to server
    conn = psycopg2.connect(database=cred.database,
                            host=cred.host,
                            user=cred.user,
                            password=cred.password,
                            port=cred.port)
    return conn


def add_items(file_name, item_name, price, date, link_id):
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO item_Listing (item_name, price, date, group_name, link_id) VALUES (%s,%s,%s,%s,%s);"""
    cursor.execute(query, (item_name, price, date, file_name, link_id))
    conn.commit()

    cursor.close()
    conn.close()


def add_links(link):
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO links (link) VALUES (%s);"""

    cursor.execute(query, (link,))
    conn.commit()

    cursor.close()
    conn.close()


def get_link_id(items, file):
    conn = connection()
    cursor = conn.cursor()

    place_holders = ', '.join(['%s'] * len(items))
    string = '%s'
    query = f"""SELECT link_id FROM item_listing WHERE item_name IN ({place_holders}) AND group_name = {string};"""
    cursor.execute(query, tuple(items)+ (file,))
    data = cursor.fetchall()
    data = [int(d[0]) for d in data]
    cursor.close()
    conn.close()

    return data


def get_attributes(file): # change this!!!
    conn = connection()
    cursor = conn.cursor()
    query = """SELECT il.item_name, il.date, ln.link, il.link_id
                FROM item_listing il
                JOIN links ln ON il.link_id = ln.id
                WHERE il.group_name = %s;"""
    cursor.execute(query, (file,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def get_prices(file):
    conn = connection()
    cursor = conn.cursor()
    query = """SELECT price
                FROM item_listing
                WHERE item_name = %s AND group_name = %s;"""
    cursor.execute(query, (file,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def get_name(file):
    conn = connection()
    cursor = conn.cursor()
    query = """SELECT group_name, item_name
                FROM item_listing
                WHERE group_name = %s;"""
    cursor.execute(query, (file,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data
# Retrieve data
# Detele a following
