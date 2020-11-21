import re 
from io import StringIO

import PyPDF2

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def convert_pdf_to_string(file_path):

	output_string = StringIO()
	with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)

	return(output_string.getvalue())

def pdf2json(file_path="Profile.pdf"):
    text = convert_pdf_to_string(file_path)
    text = text.replace('.','')
    text = text.replace('\x0c','').replace('\xa0', '')
    list_contents = text.split('\n\n\n\n')
    table_of_contents_raw = [content.split('\n') for content in list_contents]

    struct_info = {
        "Name": [],
        "Contact": [], 
        "Top Skills": [],
        "Languages": [],
        "Honors-Awards": [],
        "Summary": [],
        "Experience": [],
        "Education": []
    }

    old_idx = -1
    list_content = list(struct_info.keys())
    for table_idx, table in enumerate(table_of_contents_raw):
        if table == []:
            continue
        
        start_idx = -1
        for unit in table:
            if unit in list_content:
                start_idx = list_content.index(unit)
                continue
            if start_idx == -1:
                if old_idx == -1:
                    continue
                elif table_idx == 2:
                    start_idx = 0
                else:
                    start_idx = old_idx
            if unit == "":
                continue
            parttern = re.match(r"^Page \d+ of \d+", unit)
            if parttern is not None:
                continue
            key = list_content[start_idx]
            struct_info[key].append(unit)

        old_idx = start_idx
    return struct_info

if __name__ == "__main__":
    
    struct_info = pdf2json()
    for key in struct_info:
        print(key)
        print(struct_info[key])
        print("~~~~")

