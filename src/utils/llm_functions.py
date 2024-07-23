from datetime import datetime as dt

import pytz


NOW = dt.now(pytz.utc).astimezone(pytz.timezone('Asia/Singapore')).isoformat()

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
This is the message you will say after setting a meeting. Always maintain a positive and human-like response. 

You will generate 4 messages separated by the following delimiter: ####.  
    1. Acknowledgement message: The message you say to acknowledge the customer's request in setting a meeting. 
    2. Success message: The message you say when a meeting was set successfully. This must contain the meeting information. 
    3. Failed message: The message you say when a meeting was not set due to conflicts. You must ask the user for new information. 
    4. Error message: The message you say when you are unable to set a meeting due to unknown errors. You must ask the user to try again later. 
    
Example: 
<acknowledgement_messsage> #### <success_message> #### <failed_message> #### <error_message>
"""

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
