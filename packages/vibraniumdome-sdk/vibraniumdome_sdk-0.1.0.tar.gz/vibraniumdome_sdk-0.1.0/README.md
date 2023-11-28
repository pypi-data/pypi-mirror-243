# vibraniumdome-sdk

To start trace your OpenAI, you need to define `VIBRANIUM_DOME_BASE_URL` environment variable to point Vibranium service; if you run it locally via the basic installation:

```
export VIBRANIUM_DOME_BASE_URL=http://localhost:5001
```

Code sample:
```python
import os
import openai

from vibraniumdome_sdk import VibraniumDome

openai.api_key = os.getenv("OPENAI_API_KEY")

VibraniumDome.init(app_name="openai_test_app")

def main():
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ],
    temperature=0,
    request_timeout=5,
    user="user-123456",
    headers={"x-session-id": "abcd-1234-cdef"},)

    print(response)


if __name__ == "__main__":
    main()
```
