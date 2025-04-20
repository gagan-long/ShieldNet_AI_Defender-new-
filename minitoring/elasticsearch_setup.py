from elasticsearch import Elasticsearch
import yaml

class ShieldNetElasticSetup:
    def __init__(self):
        self.es = Elasticsearch(['http://elasticsearch:9200'])
        self.index_config = """
        {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "threat_analyzer": {
                            "tokenizer": "standard",
                            "filter": ["lowercase", "threat_filter"]
                        }
                    },
                    "filter": {
                        "threat_filter": {
                            "type": "synonym",
                            "synonyms_path": "analysis/threat_synonyms.txt"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "event_type": {"type": "keyword"},
                    "severity": {"type": "integer"},
                    "message": {
                        "type": "text",
                        "analyzer": "threat_analyzer"
                    }
                }
            }
        }
        """

    def setup_index(self):
        if not self.es.indices.exists(index="shieldnet-events"):
            self.es.indices.create(
                index="shieldnet-events",
                body=self.index_config
            )
            print("Created shieldnet-events index")
        else:
            print("Index already exists")

    def update_alert_rules(self):
        with open('monitoring/alert_rules.yaml') as f:
            rules = yaml.safe_load(f)
        
        self.es.index(
            index="alert-rules",
            id="shieldnet-rules",
            document=rules
        )

if __name__ == "__main__":
    es_setup = ShieldNetElasticSetup()
    es_setup.setup_index()
    es_setup.update_alert_rules()
