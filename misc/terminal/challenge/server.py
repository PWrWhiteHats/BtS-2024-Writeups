#!/usr/bin/env /usr/local/bin/python3
# -*- coding: utf-8 -*-

from openai import OpenAI
from limits import storage, strategies, RateLimitItemPerMinute
import json
import time
import sys


with open("config.json", "r") as f:
    config = json.load(f)

API_KEY = config["API_KEY"]


# rate limiting
memory_storage = storage.RedisStorage("redis://localhost:6379")
moving_window = strategies.MovingWindowRateLimiter(memory_storage)
limit_per_minute = RateLimitItemPerMinute(amount=350)


class FakeTerminal:
    def __init__(self) -> None:
        self.messages = [
            {
                "role": "system",
                "content": [
                    {
                        "text": open("prompt.txt", "r").read(),
                        "type": "text"
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "text": "start",
                        "type": "text"
                    }
                ]
            },
            {
                "role": "assistant",
                "content": "Last login: Mon Jul 26 15:30:00 UTC 2021\nuser@challenge:/home/user$ "
            }
        ]
        self.client = OpenAI(api_key=API_KEY)

    def get_next(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # print(response)
        text = response.choices[0].message.content

        self.messages.append({
            "role": "assistant",
            "content": text
        })

        if text[-1] != ' ':
            text += ' '

        return text

    def next(self, message: str):
        self.messages.append({"role": "user", "content": message})
        return self.get_next()
    

def main() -> None:
    terminal = FakeTerminal()
    print(terminal.messages[-1]["content"], end="")

    while True:
        if not moving_window.hit(limit_per_minute):
            print("\nSlow down a bit please :)\n")
            sys.stdout.flush()
            time.sleep(2)

            while not moving_window.test(limit_per_minute):
                print(".", end="")
                sys.stdout.flush()
                time.sleep(2)

            response = terminal.next(message)
            print("")
            print(response, end="")
            sys.stdout.flush()

            continue

        if len(terminal.messages) > 50:
            terminal.messages = terminal.messages[-50:]

        try:
            message = input()

            if len(message) > 128:
                print("Max length exceeded\n")
                message = ""
        except EOFError:
            break
        response = terminal.next(message)

        print(response, end="")


main()
