from dotenv import load_dotenv
from services.llm_service import StorybookLLMService
from services.image_service import StorybookImageService
from services.pdf_compiler import compile_storybook_pdf

load_dotenv()

def main():
    # 1. Define the STEM topic and cultural analogy for If/Else conditional logic
    topic = "Algorithmic Thinking and If/Else Conditional Logic"
    analogy = "Grandmother sorting and grading harvested yams in the farm barn based on size, ripeness, and destination."
    
    print("=" * 60)
    print(" 📚 ILLUSTRATED CULTURAL & STEM STORYBOOK GENERATOR ")
    print("=" * 60)
    print(f"STEM Topic : {topic}")
    print(f"Analogy    : {analogy}\n")

    # 2. Step 1: Generate Storyboard JSON via LLM Service (Chain-of-Thought & Pages)
    print("[1/3] Running LLM CoT Engine & Storyboard Generation...")
    llm_service = StorybookLLMService()
    storybook = llm_service.generate_storybook(stem_topic=topic, cultural_analogy=analogy)
    
    print(f" > Protagonist          : {storybook.character.name}, Age {storybook.character.age}")
    print(f" > Setting              : {storybook.character.setting}")
    print(f" > Scientific Principle : {storybook.reasoning.scientific_principle}\n")

    # 3. Step 2: Generate Consistent Illustrations for Each Page
    print("[2/3] Generating Multimodal Illustrations (Character & Style Anchored)...")
    image_service = StorybookImageService()
    image_paths = []
    
    for page in storybook.pages:
        img_filename = f"output/images/page_{page.page_number}.png"
        
        # Generates and saves the illustration for this specific page
        saved_path = image_service.generate_page_illustration(
            character=storybook.character,
            page=page,
            output_path=img_filename,
            seed=42  # Locked seed for consistency across pages
        )
        image_paths.append(saved_path)

    # 4. Step 3: Compile Text and Images into a Formatted PDF Storybook
    print("\n[3/3] Compiling Storybook PDF...")
    output_pdf_path = "output/books/algorithmic_yam_sorting_storybook.pdf"
    compile_storybook_pdf(
        storybook=storybook,
        image_paths=image_paths,
        output_filename=output_pdf_path
    )
    
    print("\n" + "=" * 60)
    print(f"✨ PIPELINE COMPLETE! Storybook saved at: {output_pdf_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()