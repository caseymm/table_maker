import os
import json
import re
import time
from datetime import datetime
import xlrd
from xlrd import open_workbook,cellname

def slugify(keyword):
    return ''.join(keyword.split(' '))

print"""
                                                                  *
                                                                 /|
_____ _   ___  _    ___  __      _____ ____  _   ___ ___        / |
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

print "Here is a example item from your spreadsheet."
print

check_float = []
for row_index in range(sheet.nrows)[starting_row:starting_row+1]:
    for col_index in range(sheet.ncols):
        print col_index, sheet.cell(row_index,col_index).value

        # Notes that the value is not a string and appends it to a list to be referenced later
        if isinstance(sheet.cell(row_index,col_index).value, float):
            check_float.append(col_index)

# Allows the user to decide which columns from the spreadsheet to keep
print
print "Please enter the index number of the columns you would like to keep. You may also type 'all' if you would like to keep all columns."
print "Format your response like this: 2,4,5,8"
keep_cols = raw_input ('>>> ')
print

if keep_cols == 'all':
    keep_cols_list = list(range(sheet.ncols))
else:
    keep_cols_list = [int(i) for i in keep_cols.split(',')]

# Section where the user names the columns that he or she has kept and is prompted to decide if they contain a number or date
col_name_dict = {}
for i in keep_cols_list:
    ival = raw_input ("Column "+str(i)+" name: ")
    date_or_num = "string"

    if i in check_float:
        print "It looks like the "+ ival +" column contains dates or numbers. If you would like to render this data as a date, type: 'date', for a number, type 'number.' Hit enter if neither."
        date_or_num = raw_input(">>> ")

        print
        print "The default date format is: ", time.strftime("%x")
        print "Would you like to use the default date format? (y/n)"
        print

        def_date = raw_input(">>> ")
        if def_date == 'y':
            d_format = '%x'
        else:
            d_format = ''
            print "Using today's date ("+time.strftime("%x")+") as an example, please answer the following questions."
            print
            print "Type how you would like 'month' to look? If you don't want to include month, hit 'ENTER.'"
            print 'ex) '+ str(time.strftime("%b"))+', '+str(time.strftime("%B"))+', '+str(time.strftime("%m"))
            def_month = raw_input(">>> ")
            def_month = def_month.capitalize()
            if def_month == str(time.strftime("%b")):
                d_format += "%b"
            elif def_month == str(time.strftime("%B")):
                d_format += "%B"
            elif def_month == str(time.strftime("%m")):
                d_format += "%m"
            else:
                add_zero = "0"+def_month
                try:
                    if add_zero == str(time.strftime("%m")):
                        d_format += "%m"
                except:
                    pass

            print
            print "Do you want to include the day? (y/n)"
            def_day = raw_input(">>> ")
            if def_day == 'y':
                d_format += "%d"
            else:
                pass

            print
            print "Type how you would like 'year' to look? If you don't want to include year, hit 'ENTER.'"
            print "ex) "+str(time.strftime("%y"))+', '+str(time.strftime("%Y"))
            def_year = raw_input(">>> ")
            if def_year == str(time.strftime("%y")):
                d_format += "%y"
            elif def_year == str(time.strftime("%Y")):
                d_format += "%Y"
            else:
                pass

        vf = [ival, date_or_num, d_format[:2]+'/%'.join(d_format[2:].split('%'))]
    else:
        vf = [ival, date_or_num]

    col_name_dict.setdefault(i, vf)

json_list = []

if ending_row == 'end':
    ending_row = sheet.nrows-1

# Generates json with correctly formatted values (string, date, number, etc.) based on the info entered above
for row_index in range(sheet.nrows)[starting_row:ending_row]:
    tmp = {}
    for col_index in col_name_dict:
        cell_val_orig = sheet.cell(row_index,col_index).value
        if col_name_dict[col_index][1] == 'date':
            try:
                formatted_dt = datetime(*xlrd.xldate_as_tuple(cell_val_orig, book.datemode))
                cell_val = datetime.strftime(formatted_dt, col_name_dict[col_index][2])
            except:
                pass
        # elif col_name_dict[col_index][1] == 'number':
        # add more formatting options here for decimal places
        # also for $ and % - check *100 for percentages
        else:
            cell_val = cell_val_orig

        tmp.setdefault(col_name_dict[col_index][0], cell_val)
    json_list.append(tmp)

json_name = raw_input ('Enter a name for your json:')
print

to_json=open(json_name+'.json','w')
jsonified = json.dumps(json_list)
print>>to_json, jsonified
to_json.close()

open_template = open('js/script_template.js','r')
open_js = open('js/script_new.js','w')
for ln in open_template:
    match = re.search(r"TABLE_HEADER", ln)
    if match:
        ln = ln.replace(match.group(0), "var col_list = "+str(list(col_name_dict[i][0] for i in col_name_dict))+";")

    match = re.search(r"json_url_here", ln)
    if match:
        ln = ln.replace(match.group(0), json_name+".json")

    match = re.search(r"CONTENT_HERE", ln)
    if match:
        ln = ln.replace(match.group(0), "")
        write_it = ''
        for t in col_name_dict:
            open_js.write("var "+slugify(col_name_dict[t][0])+" = '<td>'+element['"+col_name_dict[t][0]+"']+'</td>';\n")
            write_it += slugify(col_name_dict[t][0])+'+'
        open_js.write("$('tbody').append('<tr>'+"+write_it+"'</tr>');")

    open_js.write(ln)
open_template.close()
open_js.close()
