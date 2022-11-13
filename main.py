import requests, string, random, argparse, sys

def getRandomString(length):
    pool=string.ascii_lowercase+string.digits
    return "".join(random.choice(pool) for i in range(length))

def getRandomText(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def generate():
    number = random.randint(1000000, 9999999)
    nick = "spotify_account" + str(number)
    passw = "spotify_account" + str(number)
    email = nick+"@gmail.com"

    headers={"Accept-Encoding": "gzip",
             "Accept-Language": "en-US",
             "App-Platform": "Android",
             "Connection": "Keep-Alive",
             "Content-Type": "application/x-www-form-urlencoded",
             "Host": "spclient.wg.spotify.com",
             "User-Agent": "Spotify/8.6.26 Android/29 (SM-N976N)",
             "Spotify-App-Version": "8.6.26",
             "X-Client-Id": getRandomString(32)}
    
    payload = {"creation_point": "client_mobile",
            "gender": "male" if random.randint(0, 1) else "female",
            "birth_year": random.randint(1990, 2000),
            "displayname": nick,
            "iagree": "true",
            "birth_month": random.randint(1, 11),
            "password_repeat": passw,
            "password": passw,
            "key": "142b583129b2df829de3656f9eb484e6",
            "platform": "Android-ARM",
            "email": email,
            "birth_day": random.randint(1, 31)}
    
    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)

    if r.status_code==200:
        if r.json()['status']==1:
            return (True, email+":"+passw)
        else:
            return (False, "error, cant make the account.")
    else:
        return (False, "error, status code: "+ str(r.status_code))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="how many accounts to generate, default is 1", type=lambda x: (int(x) > 0) and int(x) or sys.exit("Invalid number: minimum amount is 1"))
    parser.add_argument("-o", "--output", help="output file, default prints to the console")
    args = parser.parse_args()

    N = args.number if args.number else 1
    file = open(args.output, "w") if args.output else sys.stdout

    print("generating accounts in the following format:\nEMAIL:PASSWORD", file=sys.stdout)
    for i in range(N):
        result = generate()
        if result[0]:
            print(result[1], file=file)
            #print(result[1], file=sys.stdout)
        else:
            print(str(i+1)+"/"+str(N)+": "+result[1], file=sys.stdout)

    if file is not sys.stdout:
        file.close()
