# gpt_interface

A simple interface for using the GPT API.

## API Key

To use gpt_interface, you need an OpenAI API key (https://platform.openai.com/docs/api-reference/authentication).

I recommend creating a .env file and adding it to your .gitignore file. The file would contain the following:

```
OPENAI_API_KEY=sk-exampleKey
```

## Simple Usage

```python
from dotenv import load_dotenv
import os
from pathlib import Path

from gpt_interface import GptInterface


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    interface = GptInterface(  # create interface
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
    )
    interface.say("Hi! My name is Matt")  # talk to GPT
    response = interface.say("What's my name?")  # conversation log is stored in memory
    assert "Matt" in response
    print(interface.log)  # can print logs
    current_path = Path(__name__).parent.absolute()
    interface.log.save(current_path / "my_log.json")  # can save or load logs
    interface.log.load(current_path / "my_log.json")
```

The log from the example above would look something like this:

```json
[
    {
        "role": "user",
        "content": "Hi! My name is Matt"
    },
    {
        "role": "assistant",
        "content": "Hello Matt! How can I assist you today?"
    },
    {
        "role": "user",
        "content": "What's my name?"
    },
    {
        "role": "assistant",
        "content": "Your name is Matt!"
    }
]
```

## Advanced Examples

See the examples/ folder to see more details about how to use the interface.
