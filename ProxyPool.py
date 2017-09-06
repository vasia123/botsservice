from datetime import datetime


class ProxyPool(object):
    __path = 'proxies'

    def __init__(self, path=None):
        if path is None:
            path = self.__path
        """Read proxy file and convert it to dict where key is current timestamp and value is proxy
        """
        with open(path) as f:
            tmp = ['http://' + line.strip() for line in f]

        self.pool = {}
        for line in tmp:
            last_usage_time = datetime.now().timestamp()
            self.pool[last_usage_time] = line

    def get_proxy(self):
        """Get last used key from self.pool dict, changes key to current time and returns proxy value
        """
        last_used_key = min(self.pool.keys())
        proxy = self.pool.pop(last_used_key)

        self.pool[datetime.now().timestamp()] = proxy

        return proxy
