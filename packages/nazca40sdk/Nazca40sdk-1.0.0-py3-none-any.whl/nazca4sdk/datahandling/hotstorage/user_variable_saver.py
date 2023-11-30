from nazca4sdk.datahandling.hotstorage.helper import transform, create_variables_frame
from nazca4sdk.datahandling.hotstorage.model.user_variable import UserVariable
from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender
from dependency_injector.wiring import inject


class UserVariableSaver:
    @inject
    def __init__(self, kafka_client: KafkaSender):
        self._kafka_sender = kafka_client

    def save_variables(self, user_variables: [UserVariable]) -> bool:
        variables = transform(user_variables)
        if len(variables) == 0:
            return False
        user_variables_frame = create_variables_frame(variables)
        return self._kafka_sender.send_message("dataflow.fct.clickhouse", 'Variables', user_variables_frame)
