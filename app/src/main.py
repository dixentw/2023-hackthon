from flask import Flask
from flask import request
import os
import openai
import sys
from logging.config import dictConfig

openai.api_key = os.getenv("OPENAI_API_KEY")
text = ""
with open("api-doc.md", "r") as f:
    text = f.read()

server = Flask(__name__)
server.config["TESTING"] = True

prompt = """
You're a JSON generator that can output a JSON payload with the given API doc and conditions.

API doc:
```
{api_doc}
```

Conditions:
```
{condition}
```

Please generate a JSON payload that satisfies the conditions above.
"""

@server.route("/", methods=["POST"])
def hello():
    print(request.get_json())
    full_prompt = prompt.format(api_doc=text, condition=request.get_json()["condition"])
    print(full_prompt)
    chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "assistant", "content": full_prompt}])
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
   server.run(host='0.0.0.0')
