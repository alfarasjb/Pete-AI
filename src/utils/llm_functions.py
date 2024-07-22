
# TODO
# Note: Just stick to JSON. It's simpler, and structure is more visible.
END_CALL_PROMPT = """
Ends the call. 
"""
END_CALL_FUNCTION = {
    "type": "function",
    "function": {
        "name": "end_call",
        "description": END_CALL_PROMPT,
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message you will say before ending the call with the customer."
                }
            },
            "required": ["message"]
        }
    }
}

CALENDLY_MEETING_MESSAGE_PROMPT = """
This is the message you will say after setting a meeting. This must contain the meeting information. 
Maintain a positive and human-like response, and end the message in an enthusiastic way. 
"""

SET_CALENDLY_MEETING_FUNCTION = {
    "type": "function",
    "function": {
        "name": "set_calendly_meeting",
        "description": "Customer request to set a Calendly meeting with PioneerDevAI.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": CALENDLY_MEETING_MESSAGE_PROMPT,
                },
                "meeting_date": {
                    "type": "string",
                    "description": "The date and time of the meeting",
                },
                "customer_name": {
                    "type": "string",
                    "description": "The name of the customer setting the meeting. The name of the customer has to be a proper noun, and a valid name. It cannot be any arbitrary placeholder such as `Customer` or `Customer Name` or `User`"
                },
                "end_call": {
                    "type": "boolean",
                    "description": "Boolean to determine if the call is finished. If the customer has no other concerns, set this as True."
                }
            },
            "required": ["message", "meeting_date", "customer_name", "end_call"]
        }
    }
}

TOOLS = [
    SET_CALENDLY_MEETING_FUNCTION,
    END_CALL_FUNCTION
]
