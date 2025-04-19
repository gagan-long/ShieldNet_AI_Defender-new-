import jsonschema

API_SCHEMA = {
    "type": "object",
    "properties": {
        "misp": {"type": "object"},
        "kafka": {"type": "object"}
    },
    "required": ["misp", "kafka"]
}

def validate_config(config):
    jsonschema.validate(instance=config, schema=API_SCHEMA)
