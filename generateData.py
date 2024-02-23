import launch

def main():
    fin = open("social-media-random-user-account-data.txt")
    for line in fin:
        words = line.split()
        email = words[0]
        username = words[1]
        password = words[2]
        launch.adduser(email)
        launch.addaccount(email, username, password)
    fin.close() 
    return -1

main()