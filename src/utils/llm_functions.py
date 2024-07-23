from datetime import datetime as dt

import pytz

from src.prompts.llm_function_prompts import END_CALL_PROMPT, CALENDLY_MEETING_MESSAGE_PROMPT


NOW = dt.now(pytz.utc).astimezone(pytz.timezone('Asia/Singapore')).isoformat()

# TODO
# Note: Just stick to JSON. It's simpler, and structure is more visible.

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

SET_CALENDLY_MEETING_FUNCTION = {
    "type": "function",
    "function": {
        "name": "set_calendly_meeting",
        "description": "Customer request to set a 30-minute consultancy meeting with PioneerDevAI.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": CALENDLY_MEETING_MESSAGE_PROMPT,
                },
                "meeting_start": {
                    "type": "string",
                    "description": f"The start date and time of the meeting in ISO 8601 format for the timezone: Asia/Singapore. This date cannot be earlier than {NOW}.",
                },
                "meeting_end": {
                    "type": "string",
                    "description": "The end date and time of the meeting in ISO 8601 format. This should be 30 minutes after the start of the meeting."
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
            "required": ["message", "meeting_start", "meeting_end", "customer_name", "end_call"]
        }
    }
}

TOOLS = [
    SET_CALENDLY_MEETING_FUNCTION,
    END_CALL_FUNCTION
]
