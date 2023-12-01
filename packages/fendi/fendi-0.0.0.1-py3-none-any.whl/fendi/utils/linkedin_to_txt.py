import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()

    return text

def convert_linkedin_pdf_to_txt(pdf_path, output_txt_path="./formatted_resume.txt"):
    # Extract text from PDF using PyMuPDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Create a dictionary to map section headers to their corresponding content
    sections = {
        'Coordonnées': 'Principales compétences',
        'Principales compétences': 'Résumé',
        'Résumé': 'Expérience',
        'Expérience': 'Formation',
        'Formation': 'Compétences Clés',
        'Compétences Clés': 'Pour plus de détails sur mon parcours et mes réalisations, je vous invite à consulter mon site web :',
        'Pour plus de détails sur mon parcours et mes réalisations, je vous invite à consulter mon site web :': ''
        # Assuming the last section continues until the end of the document
    }

    # Write the formatted content to a text file
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        for section, next_section in sections.items():
            pattern = re.compile(re.escape(section) + r'(.*?)' + re.escape(next_section), re.DOTALL)
            match = pattern.search(pdf_text)
            if match:
                section_content = match.group(1).strip()

                # Print section and content (for debugging)
                #print(f'Section: {section}\nContent: {section_content}')

                # Write the formatted content to a text file
                txt_file.write(f'**{section}**\n\n{section_content}\n\n')