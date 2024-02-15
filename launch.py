import argparse
import os
import sqlite3

DB_FILE = 'network.db'

def error(args):
    print('This command requires a subcommand')

def create(args){
    if os.path.exists(DB_FILE):
        print(DB_FILE, 'already exists, quitting')
        sys.exit(1)

    con = sqlite3.connect(DB_FILE)
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
    CREATE TABLE subsribers(
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

}

def main(){

}

main()