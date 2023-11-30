from datetime import datetime
from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender
from nazca4sdk.datahandling.knowledge.knowledge_data_type import KnowledgeDataType
from nazca4sdk.datahandling.open_data_client import OpenDataClient
from datetime import timezone
from dependency_injector.wiring import inject


class KnowledgeStorage:

    @inject
    def __init__(self, opendata_client: OpenDataClient, kafka_client: KafkaSender):
        self._opendata = opendata_client
        self._kafka_client = kafka_client

    def read_keys(self, name: str = None, ts_min: str = None, ts_max: str = None, size: int = 0) -> list:
        """ read knowledge keys

            Args:
               name: key filter
               ts_min: timestamp min
               ts_max: timestamp max
               size: max key list size
            Returns:
               key list
        """

        def validate(date):
            try:
                if date is None:
                    return True
                datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                return True
            except ValueError:
                print("Incorrect datetime format, should be YYYY-MM-DDTHH:MM:SS")
                return False

        if not validate(ts_min):
            return list()
        if not validate(ts_max):
            return list()

        if ts_min is None:
            ts_min_str = None
        else:
            dt_ts_min = datetime.strptime(ts_min, '%Y-%m-%dT%H:%M:%S')
            ts_min_str = dt_ts_min.strftime("%Y%m%dT%H%M%S")

        if ts_max is None:
            ts_max_str = None
        else:
            dt_ts_max = datetime.strptime(ts_max, '%Y-%m-%dT%H:%M:%S')
            ts_max_str = dt_ts_max.strftime("%Y%m%dT%H%M%S")

        return self._opendata.read_knowledge_keys(name, ts_min_str, ts_max_str, size)

    def read_key_values(self, key: str) -> list:
        """ read knowledge for key

               Args:
                   key: key
               Returns:
                   Knowledge
        """
        return self._opendata.read_knowledge_values(key)

    def write_key_values(self, key: str, section: str, value: str, datatype: KnowledgeDataType) -> bool:
        """Write value to knowledge

               Args:
                   key: key
                   section: section name
                   value: value
                   datatype: data type to write
               Returns: True - write success, False - write error
               """

        if not KnowledgeDataType.has_value(datatype):
            print(f"KafkaDataType has no value  {datatype}")
            return False
        current_timestamp = datetime.now(timezone.utc).isoformat()
        data_dict = {"timestamp": current_timestamp,
                     "key": key,
                     "property": section,
                     "value": value,
                     "dataType": datatype.value}
        return self._kafka_client.send_message("dataflow.fct.knowledge", key, data_dict)

    def delete_keys(self, keys) -> int:
        """ Deletes all knowledge keys for the given list

              Args:
                  keys: key list
              Returns:
                  deleted documents
              """
        return self._opendata.delete_knowledge_keys(keys)

    def delete_sections(self, sections, key) -> bool:
        """ Deletes all sections from the list from the given key

               Args:
                   sections: section list
                   key: the name of the key from which the sections are to be removed

               Returns:
                   result - true if the operation was successful, false on error
               """
        return self._opendata.delete_knowledge_sections(sections, key)
