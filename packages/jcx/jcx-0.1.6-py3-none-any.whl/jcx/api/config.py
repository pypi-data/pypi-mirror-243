from dataclasses import dataclass


@dataclass
class Endpoint:
    host: str
    port: int

    def __str__(self):
        return '%s:%d' % (self.host, self.port)


@dataclass
class ApiCfg:
    name: str
    root: str
    endpoint: Endpoint

    def url(self, scheme: str) -> str:
        """获取URL"""
        return '%s://%s/%s' % (scheme, self.endpoint, self.root)


def a_test():
    cfg = ApiCfg('配置', '/howell/ias', Endpoint('localhost', 5000))
    print(cfg)
    print(cfg.url('http'))


if __name__ == '__main__':
    a_test()
