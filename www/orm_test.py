# urf-8
import asyncio

import www.orm as orm
from www.models import User, Blog, Comment


@asyncio.coroutine
def testSave():
    yield from orm.create_pool(loop, user='admin', password='123456', db='awesome')
    u = User(name='awsome_admin', email='awsome_admin@gmail.com', passwd='1234567890', image='about:blank',admin=True)
    yield from u.save()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testSave())
    loop.close()