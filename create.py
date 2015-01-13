import os
import json
import re
from datetime import datetime
import xlrd
from xlrd import open_workbook,cellname

def slugify(keyword):
    return ''.join(keyword.split(' '))

print"""
                                                                  *
                                                                 /|
_____ _   ___ _    ___  __      _____ ____  _   ___ ___         / |
|_   _/_\ | _ ) |  | __| \ \    / /_ _|_  / /_\ | _ \   \      /  |
  | |/ _ \| _ \ |__| _|   \ \/\/ / | | / / / _ \|   / |) |   _/___|_
  |_/_/ \_\___/____|___|   \_/\_/ |___/___/_/ \_\_|_\___/  ( ______ )

  """

excel_file_path = raw_input ("Please drag file into terminal: ")

print "Does the file contain a header row? (y/n)"
header_yn = raw_input(">>> ")
accept_all = ['y', 'yes']
if header_yn in accept_all:
    starting_row = 1
else:
    starting_row = 0

print "Would you like to get a specific subset of the rows included in the spreadsheet? (y/n)"
get_rows = raw_input(">>> ")

if get_rows in accept_all:
    starting_row = raw_input ("Starting row: ")
    ending_row = raw_input ("Ending row: ")
else:
    ending_row = 'end'

#for getting base
excel_file = os.path.abspath(excel_file_path.strip(' '))

book = open_workbook(excel_file)
sheet = book.sheet_by_index(0)
# print sheet.name
# print sheet.nrows
# print sheet.ncols

# for col_index in range(sheet.ncols):
#     print col_index
print "Here is a example item from your spreadsheet."
print

for row_index in range(sheet.nrows)[starting_row:starting_row+1]:
    # print row_index
    for col_index in range(sheet.ncols):
        # print cellname(row_index,col_index),'-',
        print col_index, sheet.cell(row_index,col_index).value
        if isinstance(sheet.cell(row_index,col_index).value, float):
            print '    this is a floated number'

print
print "Please enter the index number of the columns you would like to keep. You may also type 'all' if you would like to keep all columns."
print "Format your response like this: 2,4,5,8"
keep_cols = raw_input ('>>> ')
print

if keep_cols == 'all':
    keep_cols_list = list(range(sheet.ncols))
else:
    keep_cols_list = [int(i) for i in keep_cols.split(',')]

col_name_dict = {}
for i in keep_cols_list:
    ival = raw_input ("Column "+str(i)+" name: ")
    col_name_dict.setdefault(i, ival)

    # Should really check for the different types & allow user to set formatting here

json_list = []

if ending_row == 'end':
    ending_row = sheet.nrows-1

for row_index in range(sheet.nrows)[starting_row:ending_row]:
# for row_index in range(sheet.nrows):
    tmp = {}
    for col_index in col_name_dict:
        cell_val = sheet.cell(row_index,col_index).value

        # This needs to be moved and separated from other floated numbers otherwise all will become dates
        try:
            formatted_dt = datetime(*xlrd.xldate_as_tuple(cell_val, book.datemode))
            # put in an if statement here that will allow the user to decide how to format the date
            cell_val = datetime.strftime(formatted_dt, '%x')
        except:
            pass

        tmp.setdefault(col_name_dict[col_index], cell_val)
    json_list.append(tmp)

json_name = raw_input ('Enter a name for your json:')
print
# print json.dumps(json_list)
to_json=open(json_name+'.json','w')
jsonified = json.dumps(json_list)
print>>to_json, jsonified
to_json.close()

open_template = open('js/script_template.js','r')
open_js = open('js/script_new.js','w')
for ln in open_template:
    match = re.search(r"TABLE_HEADER", ln)
    if match:
        ln = ln.replace(match.group(0), "var col_list = "+str(list(col_name_dict[i] for i in col_name_dict))+";")

    match = re.search(r"json_url_here", ln)
    if match:
        ln = ln.replace(match.group(0), json_name+".json")

    match = re.search(r"CONTENT_HERE", ln)
    if match:
        ln = ln.replace(match.group(0), "")
        write_it = ''
        for t in col_name_dict:
            open_js.write("var "+slugify(col_name_dict[t])+" = '<td>'+element['"+col_name_dict[t]+"']+'</td>';\n")
            write_it += slugify(col_name_dict[t])+'+'
        open_js.write("$('tbody').append('<tr>'+"+write_it+"'</tr>');")

    open_js.write(ln)
open_template.close()
open_js.close()
