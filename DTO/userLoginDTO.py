from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class userLoginDTO:

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def generate_auth_token(self, expiration=600):
        s = Serializer("super secret key", expires_in=expiration)
        print(s)
        return s.dumps({'username': self.username})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer("super secret key")
        print("qweqweqewq")
        try:
            data = s.loads(token)
            print(data)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        return data
