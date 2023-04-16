# custom_json_encoder.py

import json
from .options import Option  # Certifique-se de importar a classe Option

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Option):
            return obj.to_dict()
        return super(CustomJSONEncoder, self).default(obj)
