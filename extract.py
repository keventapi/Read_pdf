from PyPDF2 import PdfReader


def extract_text(title):
	title = title.replace(".pdf", "")
	readed_pdf = PdfReader(f'pdfs/{title}.pdf')
	return readed_pdf.pages
	
#	
def create_text(page, arch):
	text = arch[page].extractText()
	content = "".join(c for c in text if c is not "")
	return content
#	
if __name__ == "__main__":
	text = extract_text("exemple.pdf")
	print("".join(f"{content} \n\n\n" for content in text))