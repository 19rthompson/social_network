import sys
import random
import click
import os
import sqlite3

DB_FILE = 'network.db'

def getdb(create=False):
    if os.path.exists(DB_FILE):
        if create:
            os.remove(DB_FILE)
    else:
        if not create:
            print('no database found')
            sys.exit(1)
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con

@click.group()
def cli():
    pass
    
@click.command()
def create():
    with getdb(create=True) as con:
        con.execute(
'''CREATE TABLE blocks(
    blocked_id      INTEGER NOT NULL,
    blocker_id      INTEGER NOT NULL,

    FOREIGN KEY (blocked_id) REFERENCES accounts(account_id),
    FOREIGN KEY (blocker_id) REFERENCES accounts(account_id)
);
''')

    con.execute(
'''CREATE TABLE accounts (
    account_id      INTEGER PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    username        TEXT NOT NULL,
    password        TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
''')

    con.execute(
'''
CREATE TABLE users (
    user_id         INTEGER PRIMARY KEY,
    email           TEXT NOT NULL
);
''')

    con.execute(
'''
CREATE TABLE followers(
    follower_id INTEGER NOT NULL,
    following_id INTEGER NOT NULL,

    FOREIGN KEY (follower_id) REFERENCES accounts(account_id),
    FOREIGN KEY (following_id) REFERENCES accounts(account_id)
);
''')
    con.execute(
'''
    CREATE TABLE subscribers(
        subscriber_id INTEGER NOT NULL,
        subscribing_id  INTEGER NOT NULL,
        FOREIGN KEY (subscriber_id) REFERENCES accounts(account_id)
        FOREIGN KEY (subscribing_id) REFERENCES accounts(account_id)
    );
''')

    con.execute(
'''
CREATE TABLE posts (
    post_id         INTEGER PRIMARY KEY,
    account_id      INTEGER NOT NULL,
    content         TEXT,
    image           TEXT,
    created_at      DATE,
    hashtag         TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
''')

@click.command()
def generate():
    people = 240
    fin = open("social-media-random-user-account-data.txt")
    for line in fin:
        words = line.split()
        email = words[0]
        username = words[1]
        password = words[2]

        with getdb() as con:
            cursor = con.cursor()
            cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
            id = cursor.lastrowid
            print(f'inserted with id = {id}')
        # adduser(email)
        
        with getdb() as con:
            cursor = con.cursor()
            cursor.execute('''INSERT INTO accounts (user_id, username, password) 
                VALUES ((SELECT user_id FROM users WHERE email = ?), ?, ?)''', (email, username, password))
            id = cursor.lastrowid
            print(f'inserted with id = {id}')
        # addaccount(email, username, password)
    for i in range(1,people):
        num1 = random.randrange(1, people)
        num2 = random.randrange(1, people)
        with getdb() as con:
            if num1 != num2:
                cursor = con.cursor()
                cursor.execute('''INSERT INTO followers(follower_id, following_id)
                    VALUES ((SELECT account_id FROM accounts WHERE user_id = ?), (SELECT account_id FROM accounts WHERE user_id = ?))''', (num1, num2))
            # addaccount(email, username, password)
    for i in range(1,people):
        num3 = random.randrange(1, people)
        num4 = random.randrange(1, people)
        with getdb() as con:
            if num1 != num2:
                cursor = con.cursor()
                cursor.execute('''INSERT INTO subscribers(subscriber_id, subscribing_id)
                    VALUES ((SELECT account_id FROM accounts WHERE user_id = ?), (SELECT account_id FROM accounts WHERE user_id = ?))''', (num3, num4))
    fin.close() 

    
@click.command()
@click.argument('email')
def adduser(email):
    print('creating user with email address', email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
        id = cursor.lastrowid
        print(f'inserted with id = {id}')




@click.command()
@click.argument('email')
@click.argument('username')
@click.argument('password')
def addaccount(email, username, password):
    print('creating account with username', username, 'for email', email, 'with password', password)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO accounts (user_id, username, password) 
            VALUES ((SELECT user_id FROM users WHERE email = ?), ?, ?)''', (email, username, password))
        id = cursor.lastrow
        print(f'inserted with id = {id}')

@click.command()
@click.argument('email')
def createUser(email):
    print('creating user with email:',email)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute("""INSERT INTO users (email) VALUES (?)""",(email,))

@click.command()
def listUsers():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute("""SELECT * FROM users""")
        
        for row in cursor.fetchall():
            print(row)

@click.command()
def listAccounts():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute("""SELECT * FROM accounts""")

        for row in cursor.fetchall():
            print(row)


@click.command()
@click.argument('followerusername')
@click.argument('followeeusername')
def followAccount(followerusername,followeeusername):
    print("having:",followerusername,"follow:",followeeusername)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute("""INSERT INTO followers(follower_id,following_id)
        VALUES(
            (SELECT account_id FROM accounts WHERE accounts.username = ?),
            (SELECT account_id FROM accounts WHERE accounts.username = ?)
            )""",
        (followerusername, followeeusername))


@click.command()
@click.argument('unfollowerusername')
@click.argument('unfolloweeusername')
def unfollowAccount(unfollowerusername,unfolloweeusername):
    print("having:",unfollowerusername,"unfollow:",unfolloweeusername)
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute("""DELETE FROM followers
        WHERE
            follower_id=(SELECT account_id FROM accounts WHERE accounts.username = ?) AND
            following_id=(SELECT account_id FROM accounts WHERE accounts.username = ?)
            """,
        (unfollowerusername, unfolloweeusername))


@click.command()
@click.argument('username')
@click.argument('content')
@click.argument('image')
@click.argument('hashtag')
def createPost(username,content,image,hashtag):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute("""INSERT INTO posts (account_id,content,image,created_at,hashtag)
        VALUES((SELECT account_id FROM accounts WHERE accounts.username = ?),?,?,DATETIME('now'),?
            )
            """,
        (username,content,image,hashtag))

@click.command()
@click.argument('content')
@click.argument('image')
@click.argument('hashtag')
@click.argument("postid")
def editPost(content,image,hashtag,postid):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute(
            """UPDATE posts
            SET content = ?,
            image = ?,
            created_at = DATETIME('now'),
            hashtag = ?
            WHERE post_id = ?""",
        (content,image,hashtag,postid))
        print(content,image,hashtag,postid)

@click.command()
@click.argument('postid')
def deletePost(postid):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute(
            """DELETE FROM posts
            WHERE post_id = ?""",
        (postid,))

@click.command()
@click.argument('userid')
def displayFeed(userid):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute("""
        SELECT posts.account_id, posts.content, posts.image, posts.hashtag
        FROM accounts AS a1
        JOIN followers as f ON f.follower_id = a1.account_id
        JOIN accounts AS a2 ON f.following_id = a2.account_id
        JOIN posts ON posts.account_id = a2.account_id
        WHERE a1.user_id = ?
        """,(userid,))


@click.command()
def simpScore():
    with getdb() as con:
        cursor=con.cursor()
        cursor.execute(
'''
SELECT
    u.email,
    ( COUNT(s.subsriber_id) / COUNT(f.following_id) ) AS simpscore
FROM users AS u
JOIN accounts AS a ON
    u.user_id = a.user_id
JOIN subscribers AS s ON
    s.subscriber_id = a.account_id
JOIN followers AS f ON
    f.follower_id = a.account_id
GROUP BY u.email
ORDER BY simpscore, u.email DESC;
''')

cli.add_command(unfollowAccount)
cli.add_command(followAccount)
cli.add_command(create)
cli.add_command(generate)
cli.add_command(adduser)
cli.add_command(addaccount)
cli.add_command(simpScore)
cli.add_command(createUser)
cli.add_command(listUsers)
cli.add_command(listAccounts)
cli.add_command(createPost)
cli.add_command(editPost)
cli.add_command(deletePost)
cli.add_command(displayFeed)

cli()

def main():
    return -1
main()
