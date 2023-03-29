import sqlite3
from faker import Faker
from datetime import datetime
from random import choice

con = sqlite3.connect('social_network.db')
cur = con.cursor()
var = 'CREATE TABLE IF NOT EXISTS people(id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, age INTEGER, city TEXT, province TEXT, bio TEXT, created_at TEXT, updated_at TEXT)'
cur.execute(var)
con.commit()
con.close()

con = sqlite3.connect('social_network.db')
cur = con.cursor()

faker = Faker()
for i in range(200):
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    age = faker.random_int(min=1, max=100)
    city = faker.city()
    province = faker.state()
    bio = faker.text()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("INSERT INTO people (first_name, last_name, email, age, city, province, bio, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, email, age, city, province, bio, created_at, updated_at))
# SQL query that creates a table named 'relationships'.
create_relationships_tbl_query = """
 CREATE TABLE IF NOT EXISTS relationships
 (
 id INTEGER PRIMARY KEY,
 person1_id INTEGER NOT NULL,
 person2_id INTEGER NOT NULL,
 type TEXT NOT NULL,
 start_date DATE NOT NULL,
 FOREIGN KEY (person1_id) REFERENCES people (id),
 FOREIGN KEY (person2_id) REFERENCES people (id)
 );
"""
cur.execute(create_relationships_tbl_query)
con.commit()
con.close()

con = sqlite3.connect('social_network.db')
cur = con.cursor()
# SQL query that inserts a row of data in the relationships table.
fake = Faker()
res = cur.execute("SELECT * FROM people")
result = res.fetchall()

ids = []
for i in result:
  ids.append(i[0])

for id in ids:
  person1_id = id
  person2_id = id + 1

  # Randomly select a relationship type
  rel_type = choice(('friend', 'spouse', 'partner', 'relative'))
  # Randomly select a relationship start date between now and 50 years ago
  start_date = fake.date_between(start_date='-50y', end_date='today')
  # Add the new relationship to the DB
  cur.execute('INSERT INTO relationships(person1_id, person2_id, type, start_date) VALUES (?, ?, ?, ?)', (person1_id, person2_id, rel_type, start_date))

con.commit()
con.close()

con = sqlite3.connect('social_network.db')
cur = con.cursor()
# SQL query to get all relationships
all_relationships_query = """
SELECT person1.first_name, person2.first_name, start_date, type FROM relationships
JOIN people person1 ON person1_id = person1.id
JOIN people person2 ON person2_id = person2.id;
"""
# Execute the query and get all results
cur.execute(all_relationships_query)
all_relationships = cur.fetchall()
con.commit()
con.close()
# Print sentences describing each relationship
for person1, person2, start_date, type in all_relationships:
    print(f'{person1} has been a {type} of {person2} since {start_date}.')

