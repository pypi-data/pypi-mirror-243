from mobio.libs.olap import SingletonArgs
from mobio.libs.olap.mining_warehouse.profiling.base_session import BaseSession


class ProfilingSession(BaseSession, metaclass=SingletonArgs):
    def __init__(self, olap_uri):
        super(ProfilingSession, self).__init__(olap_uri)
