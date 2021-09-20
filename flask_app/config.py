DB_CONFIG =  {
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'PORT': 5433,
    'HOST': 'localhost',
    'DB_NAME': 'flask_bmg'
}
REDIS_CONFIG = {
    'HOST': 'localhost',
    'PORT': 6379
}
JWT_SECRET_KEY = 'y6_7#d9&l^5l5@$ob%4&kk70j@jdmq=h0b(b^9r0$9%@jn#x2%'

AUTHORIZATIONS = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description':  "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

DB_URI = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
    user=DB_CONFIG['USER'],
    password=DB_CONFIG['PASSWORD'],
    host=DB_CONFIG['HOST'],
    port=DB_CONFIG['PORT'],
    db_name=DB_CONFIG['DB_NAME'],
)

REDIS_URL = "redis://{host}:{port}".format(host=REDIS_CONFIG['HOST'], port=REDIS_CONFIG['PORT'])