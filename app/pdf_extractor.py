import re 
from io import StringIO

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

def count_year(string):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    parttern = "^(" + "|".join(months) + ")"
    start_span = re.match(rf"{parttern} \d+", string.split("-")[0]).span()
    start = string.split("-")[0][start_span[0]: start_span[1]].split()
    if "Present" in string.split("-")[1]:
        end = "November 2020".split()
    else:
        end_span = re.match(rf"{parttern} \d+", string.split("-")[1]).span()
        end = string.split("-")[1][end_span[0]: end_span[1]].split()

    num_mounths = 0
    num_years = 0
    if start[1] == end[1]:
        num_mounths = months.index(end[0]) - months.index(start[0]) + 1
    else:
        num_mounths = (len(months) + months.index(end[0]) - months.index(start[0]) + 1) % 12
    
    num_years = int(end[1]) - int(start[1]) + int(num_mounths / 12)

    return num_mounths + num_years * 12

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
    
    experiment = []
    list_times = []
    for text_idx, text in enumerate(struct_info["Experience"]):
        if text.split()[0] in ["January", "February", "March", "April", "May", "July", "August", "September", "October", "November", "December"]:
            sample = ""
            if text_idx == 2:
                sample = f"{struct_info['Experience'][0]}, {struct_info['Experience'][1]}, {struct_info['Experience'][2]}"
            else:
                if re.match(r"^\d+ (years|months|month|year)", struct_info['Experience'][text_idx - 2]) is not None:
                    sample = f"{struct_info['Experience'][text_idx - 3]}, {struct_info['Experience'][text_idx - 1]}, {struct_info['Experience'][text_idx]}"
                else:
                    sample = f"{struct_info['Experience'][text_idx - 2]}, {struct_info['Experience'][text_idx - 1]}, {struct_info['Experience'][text_idx]}"
            if sample != "" and len(experiment) <= 3:
                experiment.append(sample)
            list_times.append(count_year(text))

    num_mounth = int(sum(list_times[1:]) / len(list_times[1:]))
    num_year = int(num_mounth / 12)
    num_mounth = int(num_mounth % 12)
    struct_info["Churn Predict"] = f"{num_year} years {num_mounth} mounths"

    for _ in range(max(0, 3 - len(experiment))):
        experiment.append("")
    struct_info["Experience"] = experiment

    level = "thpt"
    for level_candidate in ["doctor", "master", "bachelor"]:
        if re.match(rf"^{level_candidate}", struct_info["Education"][1].lower()) is not None:
            level = level_candidate
            break 
    struct_info["Level"] = level

    major_list = ["computer science", "business administration", "human resources management"]
    struct_info["Majors"] = []
    for major in major_list:
        if major in ", ".join(struct_info["Education"]).lower() and major not in struct_info["Majors"]:
            struct_info["Majors"].append(major)
    
    email = ""
    for text in struct_info["Contact"]:
        if re.match("^[\w.+\-]+@gmail\.com", text) is not None:
            email = text
            break
        if re.match("^[\w.+\-]+@gmailcom", text) is not None:
            email = text
            break
        if re.match("^wwwlinkedincom/", text) is not None:
            email = text
            break
        
    struct_info["Mail"] = email

    return struct_info

def pdf2tructure(file_path):
    struct_info = pdf2json(file_path)

    struct_data = {
        "name": struct_info["Name"][0],
        "email": struct_info["Mail"],
        "phone": "",
        "address": "",
        "gender": "",
        "languages": ", ".join(struct_info["Languages"]),
        "education_level": struct_info["Level"],
        "major": ", ".join(struct_info["Majors"]),
        "university": struct_info["Education"][0],
        "age": "",
        "skills":  ", ".join(struct_info["Top Skills"]),
        "job1": struct_info["Experience"][0],
        "job2": struct_info["Experience"][1],
        "job3": struct_info["Experience"][2],
        "satisfaction": "",
        "ot": "",
        "salary_expectation": "",
        "churn_prediction": struct_info["Churn Predict"]
    }

    return struct_data
    

if __name__ == "__main__":
    struct_info = pdf2tructure("Profile.pdf")
    for key in struct_info:
        print(key)
        print(struct_info[key])
        print("~~~~")

