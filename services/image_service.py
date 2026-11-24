import os
import time
import shutil
import urllib.parse
import requests
from dotenv import load_dotenv
from schemas.storybook import CharacterSheet, StoryPage

load_dotenv()

class StorybookImageService:
    def __init__(self, fallback_image_path: str = "assets/placeholder.png"):
        self.base_url = "https://image.pollinations.ai/prompt"
        self.fallback_image_path = fallback_image_path
        self.style_anchor = (
            "vector art children book illustration, vibrant warm African color palette, "
            "textured paper background, whimsical and friendly character design, high detail"
        )

    def generate_page_illustration(self, character: CharacterSheet, page: StoryPage, output_path: str, seed: int = 42, max_retries: int = 3) -> str:
        """
        Generates and downloads a unique illustration for a single story page with 
        built-in exponential backoff retries and fallback asset handling.
        """
        # Unique seed per page so compositions vary while style/character stay locked
        page_seed = seed + page.page_number
        
        raw_prompt = (
            f"Style: {self.style_anchor}. "
            f"Character: {character.name}, age {character.age}, {character.appearance}. "
            f"Setting: {character.setting}. "
            f"Scene Action: {page.image_prompt_descriptor}."
        )
        
        encoded_prompt = urllib.parse.quote(raw_prompt)
        image_url = f"{self.base_url}/{encoded_prompt}?seed={page_seed}&width=1024&height=768&nologo=true"

        print(f"Generating illustration for Page {page.page_number}...")
        
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(image_url, timeout=45)
                if response.status_code == 200:
                    output_dir = os.path.dirname(output_path)
                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)
                    with open(output_path, "wb") as handler:
                        handler.write(response.content)
                    print(f"Successfully saved illustration to {output_path}")
                    return output_path
                else:
                    print(f"Attempt {attempt}/{max_retries}: Server returned status code {response.status_code}")
            except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"Attempt {attempt}/{max_retries} failed due to timeout or network error: {e}")
            
            if attempt < max_retries:
                sleep_time = 2 ** attempt  # 2s, 4s, 8s
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
                
        # --- Fallback Handling if All Retries Fail ---
        print(f"⚠️ Warning: All retries failed for page {page.page_number}. Using fallback asset.")
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        if os.path.exists(self.fallback_image_path):
            shutil.copy(self.fallback_image_path, output_path)
            print(f"Fallback asset copied to {output_path}")
        else:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (1024, 768), color=(245, 240, 230))
            d = ImageDraw.Draw(img)
            d.text((400, 380), f"Page {page.page_number}\n(Illustration Placeholder)", fill=(100, 100, 100))
            img.save(output_path)
            print(f"Generated default placeholder image at {output_path}")
            
        return output_path