"""SDK to communicate with Nazca4.0 system """
from dependency_injector.wiring import inject
from nazca4sdk.container import Container
from nazca4sdk.datahandling.hotstorage.clickhouse.clickhouse_client import ClickhouseClient
from nazca4sdk.datahandling.hotstorage.query import Query


class SDK:
    """SDK for Nazca4 system"""

    def __init__(self, https: bool):
        """ Initializing the system, checking connection and caching system configuration
        if https is required then https = True"""

        # nadpisuje konfiguracje
        Container.config.https.from_value(str(https))
        # print(self.c.clickhouse_client.get("Select * from nazca.test"))
        self._system_cache = Container.system_cache()
        #: :class:`nazca4sdk.analytics.analytics.Analytics` analytics functions
        self.analytics = Container.analytics()
        #: :class:`nazca4sdk.datahandling.nazcavariables.nazca_variables_storage.NazcaVariablesStorage`
        # read nazca variables
        self.nazca_variables = Container.nazca_variable_storage()
        #: :class:`nazca4sdk.system.variables.Variables` read device variables and variables statistics
        self.variables = Container.variables()
        #: :class:`nazca4sdk.system.user_variables.UserVariables` read and write user variables and user variables statistics
        self.user_variables = Container.user_variables()
        #: :class:`nazca4sdk.datahandling.knowledge.knowledge_storage` read, write and delete knowledge
        self.knowledge = Container.knowledge_storage()
        # :class:`nazca4sdk.datahandling.cache.cache_storage.CacheStorage` read and write cache value
        self.cache = Container.cache_storage()
        # :class:`nazca4sdk.system.npoe.Npoe` npoe functions
        self.npoe = Container.npoe()
        # :class:`nazca4sdk.datahandling.file.FileStorage` Communicate with files repository
        self.file_storage = Container.file_storage()
        self._clickhouse_client = Container.clickhouse_client()
        if not self._system_cache.load:
            print("Init SDK failed")

    def _get_modules(self):
        """Read all nazca4 modules

        Returns:
             (:obj:`list` of :obj:`str`) : list all modules
        """

        return self._system_cache.modules

    modules = property(_get_modules)

    def read_by_query(self, query: Query):
        """
        Reads data from hotstorage using SQL query.
        Args:
            query: <str>: SQL Query content.

        Returns: <dataframe>

        """
        query = query.strip(';')

        max_limit = 100
        if not query:
            raise ValueError("Query can't be empty.")

        if "LIMIT" not in query:
            limit = max_limit
            query = query.strip(';') + f" LIMIT {limit}"
        return self._clickhouse_client.get(query)


if __name__ == "nazca4sdk.sdk":
    container = Container()
    container.init_resources()
