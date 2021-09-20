import os

DB_CONFIG =  {
    'USER': os.environ.get('POSTGRES_USER'),
    'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    'PORT': os.environ.get('POSTGRES_PORT'),
    'HOST': os.environ.get('POSTGRES_HOST'),
    'DB_NAME': os.environ.get('POSTGRES_DB')
}
REDIS_CONFIG = {
    'HOST': os.environ.get('REDIS_HOST'),
    'PORT': os.environ.get('REDIS_PORT')
}
JWT_SECRET_KEY = 'y6_7#d9&l^5l5@$ob%4&kk70j@jdmq=h0b(b^9r0$9%@jn#x2%'

DB_URI = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
    user=DB_CONFIG['USER'],
    password=DB_CONFIG['PASSWORD'],
    host=DB_CONFIG['HOST'],
    port=DB_CONFIG['PORT'],
    db_name=DB_CONFIG['DB_NAME'],
)

REDIS_URL = "redis://{host}:{port}".format(host=REDIS_CONFIG['HOST'], port=REDIS_CONFIG['PORT'])