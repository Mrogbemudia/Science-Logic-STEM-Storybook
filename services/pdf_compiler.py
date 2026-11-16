import os
from PIL import Image
from fpdf import FPDF
from schemas.storybook import StorybookOutput

class StorybookPDFCompiler(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Optional running header for storybook pages
        pass

    def footer(self):
        # Page numbering at the bottom center
        self.set_y(-15)
        self.set_font("helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def compile_storybook_pdf(storybook: StorybookOutput, image_paths: list[str], output_filename: str = "output/books/storybook.pdf") -> str:
    """
    Compiles the 5-page storybook JSON and generated images into a formatted PDF.
    """
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    pdf = StorybookPDFCompiler(orientation="L", unit="mm", format="A4") # Landscape A4 is great for picture books
    
    # --- Title Page ---
    pdf.add_page()
    pdf.set_fill_color(245, 240, 230) # Warm cultural background tone
    pdf.rect(0, 0, 297, 210, "F")
    
    pdf.set_font("helvetica", "B", 28)
    pdf.set_text_color(40, 30, 20)
    pdf.ln(50)
    pdf.cell(0, 15, f"STEM Tales: {storybook.stem_topic}", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "I", 14)
    pdf.set_text_color(90, 80, 70)
    pdf.cell(0, 10, f"Featuring {storybook.character.name} in {storybook.character.setting}", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(20)
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 6, f"Learning Core Principle:\n{storybook.reasoning.scientific_principle}", align="C")

    # --- Story Pages (1 to 5) ---
    for idx, page in enumerate(storybook.pages):
        pdf.add_page()
        
        # Two-column layout: Left column for image, Right column for story text
        # Image Box (Left)
        img_path = image_paths[idx] if idx < len(image_paths) else None
        if img_path and os.path.exists(img_path):
            # Place image from x=15, y=20, width=130mm
            pdf.image(img_path, x=15, y=20, w=130)
            
        # Text Box (Right)
        pdf.set_xy(155, 25)
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(120, 10, f"Page {page.page_number}", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_x(155)
        pdf.set_font("helvetica", "", 13)
        pdf.set_text_color(50, 50, 50)
        # multi_cell for narrative text to handle word wrapping nicely
        pdf.multi_cell(120, 8, page.story_text)

    pdf.output(output_filename)
    print(f"Successfully compiled storybook PDF at: {output_filename}")
    return output_filename