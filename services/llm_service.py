import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schemas.storybook import StorybookOutput

load_dotenv()

class StorybookLLMService:
    def __init__(self):
        # Initialize the official Google GenAI client
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-3.8-flash"

    def generate_storybook(self, stem_topic: str, cultural_analogy: str) -> StorybookOutput:
        """
        Orchestrates the Chain-of-Thought reasoning and 5-page storybook generation
        with strict JSON schema enforcement.
        """
        prompt = f"""
        You are an expert children's STEM author and cultural educator. 
        Your task is to generate a 5-page illustrated storybook for primary school readers (ages 7-10).

        STEM Topic: {stem_topic}
        Cultural Analogy: {cultural_analogy}

        Requirements:
        1. Deconstruct the STEM topic into core logic rules.
        2. Map the rules to the cultural analogy (e.g., If yam is large and brown -> Store in barn; Else if bruised -> Sell at morning market).
        3. Write 5 engaging pages where sentences do not exceed 12 words.
        4. Provide detailed image prompt descriptors for each page, combining character descriptors and African art style anchors.
        """

        # Enforce structured JSON output matching the Pydantic StorybookOutput model
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=StorybookOutput,
                temperature=0.7,
            ),
        )

        # Validate and parse response text into the Pydantic model
        return StorybookOutput.model_validate_json(response.text)