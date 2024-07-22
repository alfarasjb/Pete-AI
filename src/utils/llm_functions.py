
# TODO
# Note: Just stick to JSON. It's simpler, and structure is more visible.
END_CALL_FUNCTION = {
    "type": "function",
    "function": {
        "name": "end_call",
        "description": "End the call if the customer explicitly requests it, or if they have no other concerns/queries.",
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
                    "description": "Friendly acknowledgement message that the meeting is set on the requested schedule. Ask a follow-up question if the customer has any more concerns."
                },
                "meeting_date": {
                    "type": "string",
                    "description": "The date and time of the meeting",
                },
                "customer_name": {
                    "type": "string",
                    "description": "The name of the customer setting the meeting. The name of the customer has to be a proper noun, and a valid name. It cannot be any arbitrary placeholder such as `Customer` or `Customer Name` or `User`"
                }
            },
            "required": ["message", "meeting_date", "customer_name"]
        }
    }
}

TOOLS = [
    SET_CALENDLY_MEETING_FUNCTION,
    END_CALL_FUNCTION
]
