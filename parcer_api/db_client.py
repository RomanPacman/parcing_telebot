import psycopg2

DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = 'admin'
HOST = 'localhost'
PORT = '5432'

FLATS_TABLE = 'flats'


def create_best_table():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS flat(
                id serial PRIMARY KEY,
                link CHARACTER VARYING(300) UNIQUE NOT NULL,
                reference CHARACTER VARYING(30),
                price INTEGER,
                title CHARACTER VARYING(1000),
                description CHARACTER VARYING(3000),
                date TIMESTAMP,
                floor CHARACTER VARYING(10),
                room INTEGER,
                apartment_area CHARACTER VARYING(10),
                phone CHARACTER VARYING(50),
                address CHARACTER VARYING(300),
                views INTEGER,
                preview CHARACTER VARYING(300)
                
                )''')


def create_table():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS flats(
                id serial PRIMARY KEY,
                link CHARACTER VARYING(300) UNIQUE NOT NULL,
                reference CHARACTER VARYING(30),
                price INTEGER,
                title CHARACTER VARYING(1000),
                description CHARACTER VARYING(3000),
                date TIMESTAMP
                )''')


def create_table_photos():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS photos (
                id serial PRIMARY KEY,
                link CHARACTER VARYING(300) UNIQUE NOT NULL,                
                flat CHARACTER (300) REFERENCES flats (link)
                )''')


# create_best_table()
# create_table()
# create_table_photos()


def insert_flat(flat):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO flats (link, reference, price,title, description, date) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                ON CONFLICT (link) DO UPDATE 
                SET title = EXCLUDED.title,
                 price = EXCLUDED.price,
                 description = EXCLUDED.description,
                 date = EXCLUDED.date''',
                        (flat.link, flat.reference, flat.price, flat.title, flat.description, flat.date))


def insert_photos(link, flat):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO photos (link, flat) 
                VALUES (%s, %s) 
                ON CONFLICT (link) DO UPDATE 
                SET 
                 flat = EXCLUDED.flat''',
                        (link, flat))


def insert_flat_realt(flat):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO flat (link, reference, price,title, description, date, floor, room, apartment_area, phone, address, views, preview) 
                VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s) 
                ON CONFLICT (link) DO UPDATE 
                SET title = EXCLUDED.title,
                 price = EXCLUDED.price,
                 description = EXCLUDED.description,
                 date = EXCLUDED.date,
                 floor = EXCLUDED.floor,
                 room = EXCLUDED.room,
                 apartment_area = EXCLUDED.apartment_area,
                 phone = EXCLUDED.phone,
                 address = EXCLUDED.address,
                 views = EXCLUDED.views,
                 preview = EXCLUDED.preview
                 ''',
                        (flat.link, flat.reference, flat.price, flat.title, flat.description, flat.date, flat.floor,
                         flat.room, flat.apartment_area, flat.phone, flat.address, flat.views, flat.preview))


def select_links():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT link FROM flat''')
            links_list = cur.fetchall()
    all_links = []
    for link in links_list:
        all_links.append(link[0])
    return all_links
