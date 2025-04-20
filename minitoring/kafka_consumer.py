from confluent_kafka import Consumer, KafkaError
import json
from elasticsearch import Elasticsearch
import yaml
from datetime import datetime

class ShieldNetConsumer:
    def __init__(self):
        self.conf = {
            'bootstrap.servers': 'kafka-broker:9092',
            'group.id': 'shieldnet-monitoring',
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.conf)
        self.es = Elasticsearch(['http://elasticsearch:9200'])
        self.alert_rules = self._load_alert_rules()

    def _load_alert_rules(self):
        with open('monitoring/alert_rules.yaml') as f:
            return yaml.safe_load(f)

    def process_event(self, msg):
        event = json.loads(msg.value())
        
        # Log to Elasticsearch
        self.es.index(
            index="shieldnet-events",
            document={
                "@timestamp": datetime.utcnow(),
                "event_type": event.get('type'),
                "severity": event.get('severity'),
                "message": event.get('message')
            }
        )

        # Check alert rules
        self._check_alert_conditions(event)

    def _check_alert_conditions(self, event):
        for rule in self.alert_rules['rules']:
            if all(event.get(k) == v for k,v in rule['conditions'].items()):
                self._trigger_alert(rule, event)

    def _trigger_alert(self, rule, event):
        # Implement your alerting logic (Slack/Email/PagerDuty)
        print(f"ALERT: {rule['name']} - {event}")
        # Example: requests.post(rule['webhook'], json=event)

    def consume(self):
        self.consumer.subscribe(['shieldnet-alerts'])
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            self.process_event(msg)

if __name__ == "__main__":
    consumer = ShieldNetConsumer()
    consumer.consume()



from dotenv import load_dotenv
load_dotenv()

conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'group.id': 'shieldnet-monitoring',
    'auto.offset.reset': 'earliest'
}