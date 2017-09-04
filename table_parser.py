import pdfplumber

pdf = pdfplumber.open("ACCS-Speisenkarte-+KW+41+.pdf")
page = pdf.pages[0]
tables = page.extract_tables()
for table in tables:
    for row in table:
        for cell in row:
            print "===="
            print cell
            print "===="
