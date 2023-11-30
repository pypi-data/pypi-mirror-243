import json
from kafka import KafkaProducer, errors


class KafkaSender:

    def __init__(self, host: str, port: str):
        self._producer = None
        self._kafka_host = host
        self._kafka_port = int(port)
        # self._producer = KafkaProducer(bootstrap_servers='10.217.1.201:10092')

    def send_message(self, topic: str, key: str, data: object):
        try:
            producer = KafkaProducer(bootstrap_servers=f'{self._kafka_host}:{self._kafka_port}')
            d = json.dumps(data)

            result = producer.send(topic=topic, key=bytes(
                key, 'utf-8'), value=str.encode(d))
            res = result.get(timeout=15)
            print(res)
            producer.flush()
            producer.close(5)
            return True
        except errors.KafkaError as e:
            print(e)
        return False
