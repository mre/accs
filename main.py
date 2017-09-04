from parser import ACCS_Menu_Parser
from datetime import date
import requests
import os.path

# Settings
filename_template = "ACCS-Speisenkarte-+KW+41+.pdf"
accs_url = "http://accs-team.de/app/download/5798435315/"
##########

week_number = date.today().isocalendar()[1]
filename = filename_template.format(week_number)

parser = ACCS_Menu_Parser(filename)
parser.pretty_print()
