import pdfquery


class ACCS_Menu_Parser():

    def __init__(self, filename):

        self.filename = filename

        # PDF files have an unusual coordinate system
        # All positions are relative to the origin at the bottom left corner
        # Our menu entries are aligned in a grid which has a certain
        # offset from the origin. The offset is given in DPI.
        self.offset_x = 97
        self.offset_y = 424

        # Box width and height
        self.width = 136
        self.height = 71

        self.days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
        self.dish_names = ["I", "II", "III", "salad", "special"]

        # We need to specify bounding boxes around the text we want to extract.
        # The formatting is always the same:
        self.bbox = 'LTTextBoxHorizontal:in_bbox("{},{},{},{}")'

        self.init_pdf()
        self.extract_menu()

    def init_pdf(self):
        self.pdf = pdfquery.PDFQuery(self.filename)
        self.pdf.load(0)
        # Debugging
        self.pdf.tree.write("dump.xml", pretty_print=True)

    def get_pos(self, i, j):
        x0 = self.offset_x + i * self.width
        y0 = self.offset_y - j * self.height
        x1 = x0 + self.width
        y1 = y0 + self.height
        return x0, y0, x1, y1

    def get_key(self, day, dish_name):
        return day + " " + dish_name

    def extract_menu(self):
        """
        Get dishes for each day.
        The positions of the dishes in the grid:
        0,0   w,0  2w,0  3w,0
        0,h   w,h  2w,h  3w,h
        0,2h  w,2h ...
        """
        # Init pdfquery statements list for data extraction
        statements = [('with_formatter', 'text')]

        for i, day in enumerate(self.days):
            for j, dish_name in enumerate(self.dish_names):
                x0, y0, x1, y1 = self.get_pos(i, j)
                key = self.get_key(day, dish_name)
                statement = (key, self.bbox.format(x0, y0, x1, y1))
                statements.append(statement)

        self.menu = self.pdf.extract(statements)

    def pretty_print(self):
        for day in self.days:
            print day
            for dish_name in self.dish_names:
                print self.menu[self.get_key(day, dish_name)]
