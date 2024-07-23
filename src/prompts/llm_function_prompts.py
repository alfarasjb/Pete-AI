"""
Set Calendly Meeting Function
"""
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

END_CALL_PROMPT = """
Ends the call. 
"""