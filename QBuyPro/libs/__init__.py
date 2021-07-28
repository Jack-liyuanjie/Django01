# --coding:utf-8--
from redis import Redis

config = {
    'host':'116.62.193.152',
    'port': 6379,
    'password': '123456',
    'db': '9',
    'decode_responses': True
}

rd_client = Redis(**config)

if __name__ == '__main__':
    rd_client.keys('*')
