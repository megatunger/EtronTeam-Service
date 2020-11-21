import PyPDF2
import data_func

reader = PyPDF2.PdfFileReader('Profile.pdf')

print(reader.documentInfo)

num_of_pages = reader.numPages
print('Number of pages: ' + str(num_of_pages))

text = data_func.convert_pdf_to_string(
    'Profile.pdf')
text = text.replace('.','')
text = text.replace('\x0c','').replace('\xa0', '')
list_contents = text.split('\n\n\n\n')
# list_contents = [text]
table_of_contents_raw = [content.split('\n') for content in list_contents]

struct_info = {
    "Contact": [], 
    "Top Skills": [],
    "Languages": [],
    "Honors-Awards": [],
    "Name": [],
    "Summary": []
}
for table in table_of_contents_raw:
    print(table)
    print("\n~~~~~\n")
# print(table_of_contents_raw[3])
