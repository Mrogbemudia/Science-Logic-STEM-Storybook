import os
import streamlit as st
from dotenv import load_dotenv

from services.llm_service import StorybookLLMService
from services.image_service import StorybookImageService
from services.pdf_compiler import compile_storybook_pdf
from services.audio_service import StorybookAudioService

load_dotenv()

st.set_page_config(
    page_title="Cultural & STEM Storybook Generator",
    page_icon="📚",
    layout="wide"
)

# App Header
st.title("📚 Illustrated Cultural & STEM Storybook Generator")
st.markdown(
    "Transform complex STEM concepts into culturally relatable African stories "
    "for primary school students using an automated LLM, image generation, audio narration, and PDF pipeline."
)

# Sidebar Controls for Customization
st.sidebar.header("📖 Story Configuration")

preset_topics = {
    "Algorithmic Thinking (If/Else Logic)": "Grandmother sorting and grading harvested yams in the farm barn based on size, ripeness, and destination.",
    "Photosynthesis (Solar Energy)": "Village sun-catchers and solar cooking pots used in an Edo State family garden.",
    "Series & Parallel Circuits": "Wiring festive market stall lights or setting up a solar phone-charging kiosk in Benin City."
}

selected_preset = st.sidebar.selectbox("Choose a Preset Topic", list(preset_topics.keys()))
custom_analogy = preset_topics[selected_preset]

stem_topic_input = st.sidebar.text_input("STEM Topic", value=selected_preset)
cultural_analogy_input = st.sidebar.text_area("Cultural Analogy & Setting", value=custom_analogy, height=100)

# --- NEW: Narrator Voice Selector in Sidebar ---
st.sidebar.header("🗣️ Audio Narration Voice")
voice_options = {
    "Nigerian (Female - Ezinne)": "en-NG-EzinneNeural",
    "Nigerian (Male - Abeo)": "en-NG-AbeoNeural",
    "Kenyan (Female - Asilia)": "en-KE-AsiliaNeural",
    "South African (Female - Leah)": "en-ZA-LeahNeural",
    "South African (Male - Luke)": "en-ZA-LukeNeural"
}
selected_voice_label = st.sidebar.selectbox("Choose Narrator Voice", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_label]

generate_btn = st.sidebar.button("✨ Generate Storybook", type="primary")

# Main Content Area
if generate_btn:
    if not os.getenv("OMNIROUTE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ Set OMNIROUTE_API_KEY or GEMINI_API_KEY in your .env file!")
    else:
        with st.status("🚀 Running Storybook Generation Pipeline...", expanded=True) as status:
            
            # Step 1: LLM Generation
            st.write("Step 1: Running Chain-of-Thought engine & storyboard generation...")
            llm_service = StorybookLLMService()
            try:
                storybook = llm_service.generate_storybook(
                    stem_topic=stem_topic_input, 
                    cultural_analogy=cultural_analogy_input
                )
                st.success(f"Storyboard generated successfully! Protagonist: {storybook.character.name}")
            except Exception as e:
                st.error(f"LLM Generation failed: {e}")
                st.stop()

            # Step 2: Image Generation
            st.write("Step 2: Generating character-consistent illustrations...")
            image_service = StorybookImageService()
            image_paths = []
            
            os.makedirs("output/images", exist_ok=True)
            for page in storybook.pages:
                img_filename = f"output/images/page_{page.page_number}.png"
                saved_path = image_service.generate_page_illustration(
                    character=storybook.character,
                    page=page,
                    output_path=img_filename,
                    seed=42
                )
                image_paths.append(saved_path)
            st.success("All 5 page illustrations anchored and generated!")

            # Step 2.5: Audio Narration Generation (Using Selected Voice)
            st.write(f"Generating voice narration ({selected_voice_label})...")
            audio_service = StorybookAudioService(voice=selected_voice_code)
            audio_paths = []
            
            os.makedirs("output/audio", exist_ok=True)
            for page in storybook.pages:
                audio_filename = f"output/audio/page_{page.page_number}.mp3"
                saved_audio = audio_service.generate_page_audio(page=page, output_path=audio_filename)
                audio_paths.append(saved_audio)
            st.success("Audio narrations generated successfully!")

            # Step 3: PDF Compilation
            st.write("Step 3: Compiling final PDF storybook...")
            os.makedirs("output/books", exist_ok=True)
            pdf_path = "output/books/generated_storybook.pdf"
            compile_storybook_pdf(storybook=storybook, image_paths=image_paths, output_filename=pdf_path)
            
            status.update(label="✅ Storybook Generation Complete!", state="complete", expanded=False)

        # Display Results in UI
        st.divider()
        st.header(f"📖 {storybook.stem_topic}")
        
        with st.expander("🔍 View Chain-of-Thought Reasoning & Character Profile"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Protagonist:** {storybook.character.name} (Age {storybook.character.age})")
                st.markdown(f"**Setting:** {storybook.character.setting}")
                st.markdown(f"**Appearance Anchor:** `{storybook.character.appearance}`")
            with col2:
                st.markdown(f"**Scientific Principle:** {storybook.reasoning.scientific_principle}")
                st.markdown(f"**Local Analogy:** {storybook.reasoning.local_analogy}")

        # Display Storyboard Pages with Audio Players
        st.subheader("Page-by-Page Storyboard & Audio Narration")
        for idx, page in enumerate(storybook.pages):
            cols = st.columns([1, 1])
            with cols[0]:
                img_p = image_paths[idx] if idx < len(image_paths) else None
                if img_p and os.path.exists(img_p):
                    st.image(img_p, caption=f"Page {page.page_number} Illustration", use_container_width=True)
                else:
                    st.info(f"[Illustration placeholder for Page {page.page_number}]")
            with cols[1]:
                st.markdown(f"### Page {page.page_number}")
                st.write(page.story_text)
                
                # Audio player for the page
                audio_p = audio_paths[idx] if idx < len(audio_paths) else None
                if audio_p and os.path.exists(audio_p):
                    st.audio(audio_p, format="audio/mp3")

                st.caption(f"**Image Prompt Descriptor:** {page.image_prompt_descriptor}")
            st.divider()

        # Download Button for PDF
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Printable PDF Storybook",
                    data=pdf_file,
                    file_name="cultural_stem_storybook.pdf",
                    mime="application/pdf"
                )
else:
    st.info("👈 Configure your topic and voice narrator in the sidebar and click **Generate Storybook** to start the pipeline.")