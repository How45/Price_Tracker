"""Imports file creds for connection & psycopg2 is to connect to postgres database"""
import psycopg2
import cred


def connection():
    """
    Gets creds to connect to server
    """
    conn = psycopg2.connect(database=cred.database,
                            host=cred.host,
                            user=cred.user,
                            password=cred.password,
                            port=cred.port)
    return conn


def add_items(file_name, item_name, price, date, link_id):
    """
    Adds the item attributes
    """
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO item_Listing (item_name, price, date, group_name, link_id) VALUES (%s,%s,%s,%s,%s);"""
    cursor.execute(query, (item_name, price, date, file_name, link_id))
    conn.commit()

    cursor.close()
    conn.close()


def add_links(link):
    """
    Adds item links to table
    """
    conn = connection()
    cursor = conn.cursor()
    query = """INSERT INTO links (link) VALUES (%s);"""

    cursor.execute(query, (link,))
    conn.commit()

    cursor.close()
    conn.close()


def get_link_id(file):
    """
    Gets the items link ids
    """
    conn = connection()
    cursor = conn.cursor()

    query = """SELECT link_id FROM item_listing WHERE group_name = %s;"""
    cursor.execute(query, (file,))
    data = cursor.fetchall()
    data = [int(d[0]) for d in data]
    cursor.close()
    conn.close()

    return data


def get_attributes(file):
    """
    Gets the item attributes
    """
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
    """
    Gets the prices of the item
    """
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
    """
    Gets the name of the item
    """
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


def delete_following(file, link_id):
    """
    Detele a following
    """
    conn = connection()
    cursor = conn.cursor()
    query_items = """DELETE FROM item_listing WHERE group_name = %s;"""
    query_link  = """DELETE FROM links WHERE id = (%s,%s);"""

    cursor.execute(query_items, (file,))
    cursor.execute(query_link, link_id)
    conn.commit()

    cursor.close()
    conn.close()


def get_group_names():
    """
    Gets all group_names
    """
    conn = connection()
    cursor = conn.cursor()
    query = """SELECT DISTINCT group_name FROM item_listing"""
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()
