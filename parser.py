import requests
import pdfquery

accs_url = "http://accs-team.de/app/download/5798435315/"
pdf_format = "ACCS-Speisenkarte-+KW+{}+.pdf"
KW = 41

def download_file(url, filename, blocksize=1024):
    with open(filename, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            return False

        for block in response.iter_content(blocksize):
            if not block:
                break
            handle.write(block)

menu_filename = pdf_format.format(KW)
menu_path = accs_url + menu_filename
#download_file(menu_path, menu_filename)

pdf = pdfquery.PDFQuery(menu_filename)
pdf.load(0) 

statements = [('with_formatter', 'text')]

# PDF files have an unusual coordinate system
# All positions are relative to the origin at the bottom left corner
# Our menu entries are aligned in a grid which has a certain
# offset from the origin. The offset is given in DPI.
offset_x = 97
offset_y = 424

# Box width and height
width = 136
height = 71 

# We need to specify bounding boxes around the text we want to extract.
# The formatting is always the same:
bbox = 'LTTextBoxHorizontal:in_bbox("{},{},{},{}")'
days = ["mo", "tu", "we", "th", "fr"]
dish_names = ["I", "II", "III", "salad", "special"]

# The positions of the dishes in the grid:
# 0,0   w,0  2w,0  3w,0
# 0,h   w,h  2w,h  3w,h
# 0,2h  w,2h ...

for i, day in enumerate(days):
    x0 = i * width + offset_x
    x1 = x0 + width
    # Get dishes for each day
    for j, dish_name in enumerate(dish_names):
        y0 = offset_y - j * height 
        y1 = y0 + height
        key = day + "_" + dish_name
        statement = (key, bbox.format(x0,y0,x1,y1))
        statements.append(statement)

menu = pdf.extract(statements)
print(menu)
#monday1 = pdf.pq('LTTextLineHorizontal:in_bbox("280,241,852,538")')
#print(monday1)

#query = pdf.pq(':contains("Gebratener")')
#for elem in query:
#    print elem.layout
