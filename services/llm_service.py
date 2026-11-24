import json
import os
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from schemas.storybook import StorybookOutput

load_dotenv()


class StorybookLLMService:
    def __init__(self):
        if OpenAI is None:
            raise RuntimeError(
                "The 'openai' package is required. Install dependencies from requirements.txt."
            )
        base_url = os.getenv("OMNIROUTE_BASE_URL", "http://localhost:20128/v1")
        api_key = os.getenv("OMNIROUTE_API_KEY", "omniroute-local")
        self.model = os.getenv("OMNIROUTE_MODEL", "welcome")
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def generate_storybook(self, stem_topic: str, cultural_analogy: str) -> StorybookOutput:
        schema_json = json.dumps(StorybookOutput.model_json_schema(), indent=2)

        system_prompt = (
            "You are an expert children's STEM educator and storyteller. "
            "Use Chain-of-Thought reasoning internally to map the STEM concept to the cultural analogy, "
            "and return ONLY valid JSON matching the exact schema provided. "
            "Every story_text sentence must have 12 words or fewer for primary school readers."
        )

        user_prompt = (
            f"Create a 5-page illustrated children's storybook.\n"
            f"STEM Topic: {stem_topic}\n"
            f"Cultural Analogy: {cultural_analogy}\n\n"
            f"Respond strictly with JSON conforming to this schema:\n{schema_json}"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        raw_content = response.choices[0].message.content
        parsed_data = json.loads(raw_content)
        return StorybookOutput.model_validate(parsed_data)