# -*- coding: utf-8 -*-
import openai

from dataclasses import dataclass

from .base import (
    LLMBase,
    ChatCompletion,
)


@dataclass
class OpenAIChatModel(LLMBase):
    name: str = "gpt-3.5-turbo"
    system_prompt: str = "You are a helpful assistant"

    def __enter__(self):
        # No special initialization required as we are using API
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # No special cleanup required as we are using API
        pass

    @property
    def ctx_size(self):
        if self.name in ("gpt-3.5-turbo", "gpt-3.5-turbo-0613"):
            return 4_000
        elif self.name in ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"):
            return 16_000
        elif self.name in ("gpt-4", "gpt-4-0613"):
            return 8_000
        elif self.name == "gpt-4-32k":
            return 32_000
        elif self.name == "gpt-4-1106-preview":
            return 128_000
        else:
            raise KeyError("Unsupported model")

    def ask(
        self,
        prompt,
        history=None,
        schema=None,
        temperature=0,
    ):
        self.sanitize_prompt(
            prompt=prompt,
            history=history,
            schema=schema,
        )

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
        ]
        if history:
            messages += history

        messages.append(
            {
                "role": "user",
                "content": prompt,
            },
        )

        kwargs = {}
        if schema:
            functions = {
                "name": "PublishAnswer",
                "description": "Publish the answer",
                "parameters": schema,
            }
            function_call = {"name": "PublishAnswer"}

            kwargs = {
                "functions": [functions],
                "function_call": function_call,
            }

        if "16k" in self.name:
            timeout = (5, 240)
        else:
            timeout = (5, 180)
        completion = openai.ChatCompletion.create(
            model=self.name,
            messages=messages,
            temperature=temperature,
            request_timeout=timeout,
            **kwargs,
        )
        return ChatCompletion.parse(completion.to_dict_recursive())
