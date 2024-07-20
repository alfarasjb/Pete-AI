import json
from dataclasses import dataclass
from typing import Dict, Any, List
from src.definitions.function_descriptions import SEND_INQUIRY_DESCRIPTION

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
    def _send_inquiry(cls) -> Dict[str, Any]:
        message = LLMFunctionProperty(
            property_type="string",
            property_description="The message you will say to acknowledge the user's request."
        )
        user_name = LLMFunctionProperty(
            property_type="string",
            property_description="The user's name."
        )
        user_message = LLMFunctionProperty(
            property_type="string",
            property_description="The user's inquiry or question for the company."
        )
        is_complete = LLMFunctionProperty(
            property_type="integer",
            property_description="""Boolean in the form of an integer, where you determine whether the email send function is to be triggered. 
                If you have any more questions, mark this as 0. If you want to trigger the function, mark this as 1."""
        )
        return LLMFunctionTemplate(
            name="send_inquiry",
            description=SEND_INQUIRY_DESCRIPTION,
            properties={
                "message": message.as_dict(),
                "user_name": user_name.as_dict(),
                "user_message": user_message.as_dict(),
                "is_complete": is_complete.as_dict()
            }
        ).as_dict()

    @classmethod
    def functions(cls) -> List[Dict[str, Any]]:
        return [
            cls._end_call_function(),
            cls._send_inquiry()
            # Add more functions here
        ]
