import os
import json
from openai import OpenAI
from ai.prompts import TEXT_PROMPT, CHOICE_PROMPT

class NVIDIAEngine:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        with open("config/profile_data.json", "r") as f:
            self.profile = json.load(f)

    def answer_question(self, question, choices=None):
        profile_str = json.dumps(self.profile)
        if choices:
            prompt = CHOICE_PROMPT.format(profile=profile_str, question=question, choices=choices)
        else:
            prompt = TEXT_PROMPT.format(profile=profile_str, question=question)

        try:
            res = self.client.chat.completions.create(
                model="meta/llama-3.1-8b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=80
            )
            return res.choices[0].message.content.strip()
        except Exception as e:
            print(f"[AI ERROR] {e}")
            return choices[0] if choices else "Yes"