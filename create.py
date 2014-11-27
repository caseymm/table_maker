import os
import json
import re
from xlrd import open_workbook,cellname

excel_file_path = raw_input ("Please drag file into terminal: ")
# starting_row = raw_input ("Starting row: ")
# ending_row = raw_input ("Ending row: ")

#for getting base
excel_file = os.path.abspath(excel_file_path.strip(' '))
print excel_file

book = open_workbook(excel_file)
sheet = book.sheet_by_index(0)
# print sheet.name
# print sheet.nrows
# print sheet.ncols

# for col_index in range(sheet.ncols):
#     print col_index
print "Here is a example item from your spreadsheet."
print

# for row_index in range(sheet.nrows)[starting_row:ending_row]:
for row_index in range(sheet.nrows)[12:13]:
    # print row_index
    for col_index in range(sheet.ncols):
        # print cellname(row_index,col_index),'-',
        print col_index, sheet.cell(row_index,col_index).value

print
print "Please enter the index number of the columns you would like to keep. You may also type 'all' if you would like to keep all columns. "
keep_cols = raw_input ('>>>')
print

if keep_cols == 'all':
    keep_cols_list = list(range(sheet.ncols))
else:
    keep_cols_list = [int(i) for i in keep_cols.split(',')]

col_name_dict = {}
for i in keep_cols_list:
    ival = raw_input ("Column "+str(i)+" name: ")
    col_name_dict.setdefault(i, ival)

json_list = []

# for row_index in range(sheet.nrows)[12:30]:
for row_index in range(sheet.nrows):
    tmp = {}
    for col_index in col_name_dict:
        tmp.setdefault(col_name_dict[col_index], sheet.cell(row_index,col_index).value)
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
            open_js.write("var "+col_name_dict[t]+" = '<td>'+element['"+col_name_dict[t]+"']+'</td>';\n")
            write_it += col_name_dict[t]+'+'
        open_js.write("$('tbody').append('<tr>'+"+write_it+"'</tr>');")

    open_js.write(ln)
open_template.close()
open_js.close()
