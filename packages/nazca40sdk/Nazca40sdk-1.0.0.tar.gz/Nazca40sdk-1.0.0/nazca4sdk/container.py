import os
from dependency_injector import containers, providers

from nazca4sdk.analytics.analytics import Analytics
from nazca4sdk.datahandling.cache.cache_storage import CacheStorage
from nazca4sdk.datahandling.file.file_storage import FileStorage
from nazca4sdk.datahandling.hotstorage.clickhouse.clickhouse_client import ClickhouseClient
from nazca4sdk.datahandling.hotstorage.user_variable_saver import UserVariableSaver
from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender
from nazca4sdk.datahandling.knowledge.knowledge_storage import KnowledgeStorage
from nazca4sdk.datahandling.nazcavariables.nazca_variables_storage import NazcaVariablesStorage
from nazca4sdk.datahandling.open_data_client import OpenDataClient
from nazca4sdk.system.npoe import Npoe
from nazca4sdk.system.system_cache import SystemCache
from nazca4sdk.system.user_variables import UserVariables
from nazca4sdk.system.variables import Variables


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    # konfiguracja zmiennych srodowiskowych
    os.environ["https"] = "False"
    # os.environ["opendata_url"] = "opendata"
    os.environ["opendata_url"] = "10.217.81.75"
    # os.environ["clickhouse_host"] = "click"
    os.environ["clickhouse_host"] = "10.217.81.75"
    # os.environ["clickhouse_port"] = "8000"
    os.environ["clickhouse_port"] = "10800"
    # os.environ["kafka_host"] = "broker"
    os.environ["kafka_host"] = "10.217.81.75"
    # os.environ["kafka_port"] = "9092"
    os.environ["kafka_port"] = "10092"
    # zapis konfiguracji ze zmiennych srodowiskowych
    config.https.from_env("https")
    config.opendata_url.from_env("opendata_url")
    config.clickhouse_host.from_env("clickhouse_host")
    config.clickhouse_port.from_env("clickhouse_port")
    config.kafka_host.from_env("kafka_host")
    config.kafka_port.from_env("kafka_port")
    # singleton
    clickhouse_client = providers.Singleton(ClickhouseClient,
                                            host=config.clickhouse_host,
                                            port=config.clickhouse_port)
    opendata_client = providers.Singleton(OpenDataClient,
                                          https=config.https,
                                          url=config.opendata_url)
    kafka_client = providers.Singleton(KafkaSender, host=config.kafka_host, port=config.kafka_port)
    system_cache = providers.Singleton(SystemCache, opendata_client=opendata_client)
    # fabryki
    cache_storage = providers.Factory(CacheStorage, opendata_client=opendata_client)
    nazca_variable_storage = providers.Factory(NazcaVariablesStorage, opendata_client=opendata_client)
    knowledge_storage = providers.Factory(KnowledgeStorage,
                                          opendata_client=opendata_client,
                                          kafka_client=kafka_client)
    npoe = providers.Factory(Npoe, opendata_client=opendata_client, cache=system_cache, click=clickhouse_client,
                             broker=kafka_client)
    user_variable_saver = providers.Factory(UserVariableSaver, kafka_client=kafka_client)
    user_variables = providers.Factory(UserVariables,
                                       click=clickhouse_client,
                                       user_variable_saver=user_variable_saver)
    variables = providers.Factory(Variables, cache=system_cache, click=clickhouse_client)
    analytics = providers.Factory(Analytics, cache=system_cache)
    file_storage = providers.Factory(FileStorage, opendata_client=opendata_client)
