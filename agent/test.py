from pypdf import PdfReader


reader = PdfReader("./output/resumes/Apple/AI Engineer.pdf")
txt = ""
for page in reader.pages:
    txt += page.extract_text()
print(txt)