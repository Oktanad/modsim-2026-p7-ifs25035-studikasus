import json
import re

def parse_llm_response(result):
    try:
        choices = result.get("choices")
        if not choices:
            raise Exception(f"Tidak ada 'choices' di response: {result}")

        content = choices[0]["message"]["content"].strip()

        if not content:
            raise Exception("Content dari LLM kosong")

        content = re.sub(r"```json\s*|\s*```", "", content).strip()

        parsed = json.loads(content)
        return parsed.get("questions", [])

    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON dari LLM: {str(e)}\nContent: {content}")
    except Exception as e:
        raise Exception(f"Parse error: {str(e)}")