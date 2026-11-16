import os
import asyncio
import edge_tts
from schemas.storybook import StoryPage

class StorybookAudioService:
    def __init__(self, voice: str = "en-NG-EzinneNeural"):
        """
        Initializes the Text-to-Speech service.
        Recommended voices for cultural authenticity:
        - 'en-NG-EzinneNeural' (Nigerian English - Female, warm storytelling tone)
        - 'en-NG-AbeoNeural'   (Nigerian English - Male)
        - 'en-KE-AsiliaNeural' (Kenyan English - Female)
        """
        self.voice = voice

    async def _synthesize_async(self, text: str, output_path: str) -> None:
        communicate = edge_tts.Communicate(text=text, voice=self.voice, rate="-5%")
        await communicate.save(output_path)

    def generate_page_audio(self, page: StoryPage, output_path: str) -> str:
        """
        Generates an MP3 narration file for a single story page.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        print(f"Generating audio narration for Page {page.page_number}...")

        try:
            asyncio.run(self._synthesize_async(page.story_text, output_path))
            print(f"Saved audio narration to {output_path}")
        except Exception as e:
            print(f"Error generating audio for Page {page.page_number}: {e}")

        return output_path