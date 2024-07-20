import json
from dataclasses import dataclass
from typing import Dict, Any

# TODO


@dataclass
class LLMFunctionProperty:
    property_name: str
    property_type: str
    property_description: str


@dataclass
class LLMFunction:
    name: str
    description: str
    properties: Dict[str, Any]

    def as_json(self):
        parameters = dict(type="object", properties=self.properties, required=list(self.properties.keys()))
        func = dict(name=self.name, description=self.description, parameters=parameters)
        return json.dumps(dict(type="function", function=func), indent=4)


# CALL THIS LATER
END_CALL_FUNCTION = LLMFunction(
    name="end_call",
    description="End the call only when the user explicitly requests it.",
    properties={
        "message": {
            "type": "string",
            "description": "The message you will say before ending the call with the customer."
        }
    }
).as_json()
