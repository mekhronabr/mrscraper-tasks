import requests
import json
import re
import ast
from typing import Tuple, Dict, Any


def natural_lang_processing(user_query):
    prompt = open("prompt.txt", encoding="utf-8").read()
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": "nousresearch/deephermes-3-mistral-24b-preview:free",
                "messages": [
                    {
                        "role": "system",
                        "content": prompt,
                    },
                    {
                        "role": "user",
                        "content": user_query,
                    },
                ],
            }
        ),
    )
    with open('data.json', 'w') as f:
        f.write(str(response.json()))
    return response.json()['choices'][0]['message']['content']


def build_args(llm_response: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse an LLM response of the form:
      search_by = "ranch"
      params = {
          "herd_code": "CC'S"
      }
    and return the tuple (search_by, params_dict).
    """
    # 1. Extract search_by value
    m = re.search(r'search_by\s*=\s*["\'](.+?)["\']', llm_response)
    if not m:
        raise ValueError("Could not find search_by assignment")
    search_by = m.group(1)

    # 2. Extract the literal params dict text
    m = re.search(r"params\s*=\s*(\{.*\})", llm_response, flags=re.DOTALL)
    if not m:
        raise ValueError("Could not find params assignment")
    params_str = m.group(1)

    # 3. Safely evaluate the dict
    try:
        params = ast.literal_eval(params_str)
    except Exception as e:
        raise ValueError(f"Failed to parse params dict: {e}")

    if not isinstance(params, dict):
        raise ValueError("Parsed params is not a dict")

    return search_by, params


def get_args_from_users_prompt(prompt):
    return build_args(natural_lang_processing(prompt))
