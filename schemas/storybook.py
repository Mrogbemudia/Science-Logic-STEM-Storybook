from typing import List
from pydantic import BaseModel, Field


class CharacterSheet(BaseModel):
    name: str = Field(..., description="Name of the protagonist")
    age: int = Field(..., description="Age of the protagonist, e.g., 9")
    appearance: str = Field(..., description="Immutable physical attributes for image prompt consistency (e.g., hair style, clothing, facial features)")
    setting: str = Field(..., description="The cultural setting, e.g., rural market town in Edo State, Nigeria")


class ChainOfThoughtReasoning(BaseModel):
    scientific_principle: str = Field(..., description="Decomposed core mechanics of the STEM topic")
    local_analogy: str = Field(..., description="Everyday African cultural/local analogy mapped to the principle")
    narrative_arc_5_part: List[str] = Field(..., description="List of 5 beats: Introduction, Inciting Incident, Exploration, Climax, Resolution")


class StoryPage(BaseModel):
    page_number: int = Field(..., ge=1, le=5, description="Page number from 1 to 5")
    story_text: str = Field(..., description="Narrative text for this page, constrained to primary reading level and max 12 words per sentence")
    image_prompt_descriptor: str = Field(..., description="Scene-specific visual action combined with the character sheet and style anchors")


class StorybookOutput(BaseModel):
    stem_topic: str = Field(..., description="The chosen STEM topic, e.g., Photosynthesis")
    character: CharacterSheet
    reasoning: ChainOfThoughtReasoning
    pages: List[StoryPage] = Field(..., min_items=5, max_items=5, description="Exactly 5 pages of the storybook")