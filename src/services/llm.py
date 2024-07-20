import json
from typing import List, Dict

from openai import AsyncOpenAI

from src.definitions.credentials import Credentials, EnvVariables
from src.prompts.prompts import BEGIN_SENTENCE, SYSTEM_PROMPT
from src.services.email_sender import send_email
from src.utils.custom_types import (
    ResponseRequiredRequest,
    ResponseResponse,
    Utterance
)
from src.utils.llm_functions import LLMFunctions

# TODO: Make function calling more robust


class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=Credentials.openai_api_key())

    @staticmethod
    def draft_begin_message() -> ResponseResponse:
        response = ResponseResponse(
            response_id=0,
            content=BEGIN_SENTENCE,
            content_complete=True,
            end_call=False
        )
        return response

    @staticmethod
    def convert_transcript_to_openai_messages(
            transcript: List[Utterance]
    ) -> List[Dict[str, str]]:
        messages = []
        for utterance in transcript:
            if utterance.role == "agent":
                messages.append({"role": "assistant", "content": utterance.content})
            else:
                messages.append({"role": "user", "content": utterance.content})
        return messages

    def prepare_prompt(
            self, request: ResponseRequiredRequest
    ) -> List[Dict[str, str]]:
        prompt = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        transcript_messages = self.convert_transcript_to_openai_messages(transcript=request.transcript)

        for message in transcript_messages:
            prompt.append(message)

        if request.interaction_type == "reminder_required":
            prompt.append({
                "role": "user",
                "content": "(Now the user has not responded in a while, you would say:)",
            })
        return prompt

    async def draft_response(
            self, request: ResponseRequiredRequest
    ) -> ResponseResponse:
        prompt = self.prepare_prompt(request)
        func_call = None
        func_arguments = ""

        stream = await self.client.chat.completions.create(
            model=EnvVariables.chat_model(),
            messages=prompt,
            stream=True,
            tools=LLMFunctions.functions()
        )
        async for chunk in stream:
            # Extract the functions
            if len(chunk.choices) == 0:
                continue
            if chunk.choices[0].delta.tool_calls:
                tool_calls = chunk.choices[0].delta.tool_calls[0]
                if tool_calls.id:
                    if func_call:
                        # Another function received. old function complete. Can break here
                        break
                    func_call = {
                        "id": tool_calls.id,
                        "func_name": tool_calls.function.name or "",
                        "arguments": {}
                    }
                else:
                    # Append Argument
                    func_arguments += tool_calls.function.arguments or ""
            # Parse transcript
            if chunk.choices[0].delta.content is not None:
                response = ResponseResponse(
                    response_id=request.response_id,
                    content=chunk.choices[0].delta.content,
                    content_complete=False,
                    end_call=False
                )
                yield response

        if func_call:
            # TODO: Improve validation
            if func_call['func_name'] == 'end_call':
                func_call['arguments'] = json.loads(func_arguments)
                response = ResponseResponse(
                    response_id=request.response_id,
                    content=func_call['arguments']['message'],
                    content_complete=True,
                    end_call=True
                )
                yield response
            elif func_call['func_name'] == 'send_inquiry':
                func_call['arguments'] = json.loads(func_arguments)
                response = ResponseResponse(
                    response_id=request.response_id,
                    content=func_call['arguments']['message'],
                    content_complete=True,
                    end_call=False
                )
                is_complete = func_call['arguments']['is_complete']
                print(f"Is complete: {is_complete}")
                if int(is_complete):
                    user_name = func_call['arguments']['user_name']
                    user_message = func_call['arguments']['user_message']
                    send_email(name=user_name, message=user_message)
                yield response
        else:
        # Send final response with "content_complete" set to True to signal completion
            response = ResponseResponse(
                response_id=request.response_id,
                content="",
                content_complete=True,
                end_call=False,
            )
            yield response
