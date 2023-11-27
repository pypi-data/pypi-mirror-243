import http.client
import datetime
import jwt

token_details = {"token": "", "expiry": ""}


def tokengeneration(url, client_id, client_secret):
    current_time_utc = datetime.datetime.utcnow()
    formatted_time = current_time_utc.strftime('%Y-%m-%d %H:%M:%S')
    if token_details["token"] == "" or token_details["expiry"] < formatted_time:
        print("entered token regeneration")
        conn = http.client.HTTPSConnection(url)
        payload = "clientId=" + client_id + "&" "clientSecret=" + client_secret
        headers = {
            'AUTH_COOKIE': '1634546337.139.324.65458',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'AUTH_COOKIE=1663132096.438.8422.634494|09d85645d3393accb9766216f4aa3fc4; LOGIN_COOKIE=1674571736.129.29.465911|6215ab38db341c1677dfbe9882af3be1'
        }
        conn.request("POST", "/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        i = data.index(":")
        j = data.index(",")
        token_details["token"] = "Bearer " + data[i + 2:j - 1]
        claims = jwt.decode(data[i + 2:j - 1], options={"verify_signature": False})
        expiry = claims['exp']
        dt_object = datetime.datetime.fromtimestamp(expiry)
        expiry_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        token_details["expiry"] = expiry_time
        return token_details["token"]
    else:
        return token_details["token"]