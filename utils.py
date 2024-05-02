import pytz
from datetime import datetime, timedelta
from settings import HOST, REDIS_PORT, SECRET_KEY, ALGORITHM, SENDER_EMAIL, SENDER_PASSWORD, REDIS_URL
from datetime import datetime, timedelta
import pytz
from jose import jwt


class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.now(pytz.utc) + timedelta(hours=1), iat=datetime.now(pytz.utc))
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.JWTError as e:
            print(e)
 