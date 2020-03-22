def get_usernames():
    res = []
    f = open("usernames.txt", "r")
    username = f.readline()
    while username:
        res.append(username.replace('\n', ''))
        username = f.readline()
    return res

