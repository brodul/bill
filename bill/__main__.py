#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
from os import listdir
from os.path import join as path_join
import csv

from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import easyxf

#STOLPEC Z REFERENCO
C_REF = 0

#STOLPEC_KOLIKO_JE_ZA_PLACAT 
C_TO_PAY= 19


def filter_reference(str_):
    """docstring for filter_ref"""
    str_ = str_.split()[-1].replace('-','')[:-1].lstrip('0')
    return str_

def search_duplicates(filename):
    file_ = open(filename, 'rb')

    csvf = csv.DictReader(file_, delimiter='#')

    dict_ = [x for x in csvf]

    odobr = [filter_reference(r["REF_ODOBR"]) for r in dict_]
    c = Counter(odobr)
    slabe = [i for i,j in c.items() if j > 1]

    uniques = []
    duplicates = []
    for i in dict_:
        if filter_reference(i["REF_ODOBR"]) in slabe:
            duplicates.append(i)
        else:
            uniques.append(i)

    return uniques, duplicates

def check_uniques(workbook, uniques, duplicates):
    rn = easyxf('pattern: pattern solid, fore_colour red')
    rp = easyxf('pattern: pattern solid, fore_colour green')

    wb = open_workbook(workbook)
    output = copy(wb)
    sheet = wb.sheet_by_index(0)
    out_sheet = output.get_sheet(0)

    C_OFFSET = sheet.ncols + 1
    R_OFFSET = sheet.nrows + 1

    nonmaching = uniques[:]
    num_payed = 0

    out_sheet.write(0, C_OFFSET, "Placal 1=DA 0=NE")
    out_sheet.write(0, C_OFFSET + 3, "Koliko je placal?")
    out_sheet.write(0, C_OFFSET + 4, "Je to dovolj?")
    out_sheet.write(0, C_OFFSET + 5, "Datum placila")
    # excel loop
    for row in range(1, sheet.nrows):
        value = sheet.cell(row, C_REF).value
        # uniques loop
        for unique in uniques:
            reference = filter_reference(unique['REF_ODOBR'])
            out_sheet.write(row, C_OFFSET, 0, rn)
            if reference == value:
                out_sheet.write(row, C_OFFSET, 1, rp)
                num_payed += 1
                out_sheet.write(row, C_OFFSET + 5 ,unique['DATUM_VAL'])

                value_to_pay = float(sheet.cell(row, C_TO_PAY).value)
                income = float(unique['ZNESEK_V_DOBRO'].replace(',', '.'))
                out_sheet.write(row, C_OFFSET + 3, income)
                #print income, value_to_pay
                if income == value_to_pay:
                    out_sheet.write(row, C_OFFSET + 4, 'OK', rp)
                else:
                    out_sheet.write(row, C_OFFSET + 4, 'Premalo', rn)
                del nonmaching[nonmaching.index(unique)]
                break

    out_sheet.write(R_OFFSET + 1, 0 , "Informacije")
    out_sheet.write(R_OFFSET + 2, 0 , "Stevilo podvojenih referenc: %s" % len(duplicates))
    out_sheet.write(R_OFFSET + 3, 0 , "Stevilo edinstvenih referenc: %s" % len(uniques))
    out_sheet.write(R_OFFSET + 4, 0 , "Stevilo placnikov: %s" % num_payed)
    out_sheet.write(R_OFFSET + 5, 0 , "Stevilo referenc, ki jih ne morem dolociti: %s" % len(nonmaching))


    out_sheet.write(R_OFFSET + 7, 0 , "Reference ki se ponavljajo (te placnike ne preverjamo) preveri rocno")
    out_sheet.write(R_OFFSET + 8, 0 , "Datum validacije")
    out_sheet.write(R_OFFSET + 8, 1 , "Naziv placnika")
    out_sheet.write(R_OFFSET + 8, 2 , "Placani znesek")
    out_sheet.write(R_OFFSET + 8, 3 , "Refereca")

    for index, payment in enumerate(duplicates):
        row = R_OFFSET + 9 + index
        out_sheet.write(row, 0 ,payment['DATUM_VAL'])
        out_sheet.write(row, 1 ,payment['NAZIV_NAL_PREJ'])
        out_sheet.write(row, 2 ,payment['ZNESEK_V_DOBRO'])
        out_sheet.write(row, 3 ,payment['REF_ODOBR'])

    R_OFFSET = R_OFFSET + 9 + len(duplicates)

    out_sheet.write(R_OFFSET + 1, 0 , "Reference ki jih sestem ni moral najti. poisci jih rocno")
    out_sheet.write(R_OFFSET + 2, 0 , "Datum validacije")
    out_sheet.write(R_OFFSET + 2, 1 , "Naziv placnika")
    out_sheet.write(R_OFFSET + 2, 2 , "Placani znesek")
    out_sheet.write(R_OFFSET + 2, 3 , "Refereca")

    for index, payment in enumerate(nonmaching):
        row = R_OFFSET + 3 + index
        out_sheet.write(row, 0 ,payment['DATUM_VAL'])
        out_sheet.write(row, 1 ,payment['NAZIV_NAL_PREJ'])
        out_sheet.write(row, 2 ,payment['ZNESEK_V_DOBRO'])
        out_sheet.write(row, 3 ,payment['REF_ODOBR'])

    output.save(path_join('rezultat','rezultat.xls'))


if __name__ == '__main__':
    uniques, duplicates = search_duplicates(path_join('abacom', listdir('abacom/')[0]))
    check_uniques(path_join('excel', listdir('excel/')[0]), uniques, duplicates)
