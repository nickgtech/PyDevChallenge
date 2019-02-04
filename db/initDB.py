import sqlite3

# Initialize a Database to use for local Dev.
# DB can be deleted and configured to MYSqlDb if setup on pc.



sqlite_file = 'ggiphy.db'

table_one = """ CREATE TABLE IF NOT EXISTS user (
                                        username TEXT PRIMARY KEY,
                                        password TEXT NOT NULL,
                                        authenticated INTEGER NOT NULL
                                    ); """
table_two = """ CREATE TABLE IF NOT EXISTS user_gifs (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        username TEXT NOT NULL,
                                        gif_url TEXT NOT NULL,
                                        category INTEGER NOT NULL,
                                        FOREIGN KEY(username) REFERENCES user (username)
                                    ); """
table_three = """ CREATE TABLE IF NOT EXISTS keys (
                                        name TEXT PRIMARY KEY,
                                        key TEXT NOT NULL
                                    ); """

key_insert = """ INSERT INTO keys (name, key) VALUES ('API_KEY', 'dc6zaTOxFJmzC'),
                                                    ('RECAPTCHA_PRIVATE_KEY', '6LdqyI0UAAAAAO4vjAs7b69ETiPhebt2bA6fnaRd'), 
                                                    ('RECAPTCHA_PUBLIC_KEY', '6LdqyI0UAAAAAPHGB46kWdKsoR_AGld2ZZTR3Xbo'),
                                                    ('SECRET_KEY', 'olyMolyItsASecret')"""

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Execute the queries to stage the data for commits
c.execute(table_one)
c.execute(table_two)
c.execute(table_three)
c.execute(key_insert)

# commit the changes to the db and then close the connection
conn.commit()
conn.close()