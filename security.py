import jwt 

def encode(username, jwt_secret, algo):
    payload = {
        "sub": username,
        "role": "ADMIN"
    }
    return jwt.encode(payload, jwt_secret, algo)

def decode(token, jwt_secret, algo):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[algo])
        if not payload.get("sub"):
            return "Error"
        return payload
    except:
        return "Error"
         