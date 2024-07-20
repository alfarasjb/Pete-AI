import json
from dataclasses import dataclass
from typing import Dict, Any, List

# TODO


@dataclass
class LLMFunctionProperty:
    property_type: str
    property_description: str

    def as_dict(self):
        values = dict(type=self.property_type, description=self.property_description)
        return values


@dataclass
class LLMFunctionTemplate:
    name: str
    description: str
    properties: Dict[str, Any]

    def as_dict(self) -> Dict[str, Any]:
        parameters = dict(type="object", properties=self.properties, required=list(self.properties.keys()))
        func = dict(name=self.name, description=self.description, parameters=parameters)
        return dict(type="function", function=func)


class LLMFunctions:

    @classmethod
    def _end_call_function(cls) -> Dict[str, Any]:
        return LLMFunctionTemplate(
            name="end_call",
            description="End the call only when the user explicitly requests it.",
            properties={
                "message": LLMFunctionProperty(
                    property_type="string",
                    property_description="The message you will say before ending the call with the customer.").as_dict()
            }
        ).as_dict()

    @classmethod
    def functions(cls) -> List[Dict[str, Any]]:
        return [
            cls._end_call_function(),
            # Add more functions here
        ]
