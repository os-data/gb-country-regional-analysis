#############################################################
# Tidies up two CRA2010 Excel tables into a single csv file.
# Table 9 has regional breakdown, while table 10 has COFOG2 codes.
# This script combines them and deals with inconsistencies.
#############################################################
import copy
import csv
import json
import logging
import re
import sys

import xlrd

from cofog import Cofog
from cra_cofog_mapper import CRACofogMapper

log = logging.getLogger(__name__)

# Global Cofog helper objects
cofog = None
cra_cofog_mapper = None

AMOUNT_MULTIPLIER = 1E6

def tidy_and_decode(x):
    '''
    Clean up Excel rows.
    '''
    return unicode(str(x).decode("mac_roman").strip())

def clean_region(region):
    '''
    Put region names in standard format.
    Keys are CRA2010 region names, values are CRA2009 names.
    '''
    standard_names = {
        'ENGLAND_Yorkshire and the Humber': 'ENGLAND_Yorkshire and The Humber',
        'Northern Ireland': 'NORTHERN IRELAND',
        'Not Identifiable': 'NOT IDENTIFIABLE',
        'Not identifiable': 'NOT IDENTIFIABLE',
        'Outside UK': 'OUTSIDE UK',
        'Scotland': 'SCOTLAND',
        'Wales': 'WALES' }
    if region in standard_names:
        region = standard_names[region]
    return region

def func_subfunc_from_hmt(func_orig, subfunc_orig):
    func = func_orig.split(" - ")[-1].strip()
    subfunc = subfunc_orig.split(" - ")[-1].strip()

    # Unusual cases that CofogMapper can't easily deal with
    if subfunc_orig[:4] == "10.4":
        subfunc = "of which: family benefits, income support and tax credits (family and children)"
    elif subfunc_orig[:4] == "10.7":
        subfunc = "of which: family benefits, income support and tax credits (social exclusion n.e.c.)"

    return func, subfunc

def cofog_from_hmt(func_orig, subfunc_orig):
    func, subfunc = func_subfunc_from_hmt(func_orig, subfunc_orig)

    cofog_parts = cra_cofog_mapper.fix(func, subfunc)

    assert len(cofog_parts) >= 1, "COFOG should have at least 1 part: [%s, %s] -> %s" % (func, subfunc, cofog_parts)
    assert len(cofog_parts) <= 3, "COFOG should have no more than 3 parts: [%s, %s] -> %s" % (func, subfunc, cofog_parts)

    cofog_parts_all = []

    for i in range(3):
        try:
            cofog_parts_all.append(cofog_parts[i])
        except IndexError:
            cofog_parts_all.append('')

    cofog_names_all = []
    for code in cofog_parts_all:
        if code:
            cofog_names_all.append(cofog[code]['description'])
        else:
            cofog_names_all.append('')

    return cofog_parts_all, cofog_names_all


def wdmmg_color(code):
    if code:
        try:
            return cofog[code]['color']
        except KeyError:
            parent_code = cofog[code]['parent']
            return wdmmg_color(parent_code)
    else:
        return ''

def make_uid_generator():
  ids = {}
  def get_id_for_year(year):
      if year in ids:
          ids[year] += 1
      else:
          ids[year] = 0
      return '%s-%s' % (year, ids[year])
  return get_id_for_year

uid_generator = make_uid_generator()

def cra2010_clean(config, out=sys.stdout):
    global cofog, cra_cofog_mapper

    cofog = Cofog(config.data_file('cofog'), config.data_file('cofog_dejargonise'))
    cra_cofog_mapper = CRACofogMapper(json.load(config.data_file('cra_cofog_map')))

    ###############################################
    # Load up original data.
    ###############################################
    sheet9 = xlrd.open_workbook(file_contents=config.data_file('cra2010_table9').read())
    table9 = sheet9.sheet_by_index(0)
    entries9 = []

    table10 = xlrd.open_workbook(file_contents=config.data_file('cra2010_table10').read())
    table10 = table10.sheet_by_index(0)
    entries10 = []

    for row in range(1, table9.nrows):
        fields = {}
        fields['dept_code'] = tidy_and_decode(table9.cell(row,0).value)
        fields['dept_name'] = tidy_and_decode(table9.cell(row,1).value)
        fields['cofog_1'] = tidy_and_decode(table9.cell(row,2).value)
        fields['hmt_1'] = tidy_and_decode(table9.cell(row,3).value)
        fields['pog'] = tidy_and_decode(table9.cell(row,4).value)
        fields['pog_alias'] = tidy_and_decode(table9.cell(row,5).value)
        fields['id_or_non_id'] = tidy_and_decode(table9.cell(row,6).value)
        fields['cap_or_cur'] = tidy_and_decode(table9.cell(row,7).value)
        fields['cg_lg_or_pc'] = tidy_and_decode(table9.cell(row,8).value)
        fields['nuts_region']  = clean_region(tidy_and_decode(table9.cell(row,9).value))
        fields['spending_04_05'] = tidy_and_decode(table9.cell(row,10).value)
        fields['spending_05_06'] = tidy_and_decode(table9.cell(row,11).value)
        fields['spending_06_07'] = tidy_and_decode(table9.cell(row,12).value)
        fields['spending_07_08'] = tidy_and_decode(table9.cell(row,13).value)
        fields['spending_08_09'] = tidy_and_decode(table9.cell(row,14).value)
        fields['spending_09_10'] = tidy_and_decode(table9.cell(row,15).value)
        fields['spending_10_11'] = tidy_and_decode(table9.cell(row,16).value)
        entries9.append(fields)

    for row in range(1, table10.nrows):
        fields = {}
        fields['dept_code'] = tidy_and_decode(table10.cell(row,0).value)
        fields['dept_name'] = tidy_and_decode(table10.cell(row,1).value)
        fields['cofog_1'] = tidy_and_decode(table10.cell(row,2).value)
        fields['hmt_1'] = tidy_and_decode(table10.cell(row,3).value)
        fields['cofog_2'] = tidy_and_decode(table10.cell(row,4).value)
        fields['hmt_2'] = tidy_and_decode(table10.cell(row,5).value)
        fields['pog'] = tidy_and_decode(table10.cell(row,6).value)
        fields['pog_alias'] = tidy_and_decode(table10.cell(row,7).value)
        fields['id_or_non_id'] = tidy_and_decode(table10.cell(row,8).value)
        fields['cap_or_cur'] = tidy_and_decode(table10.cell(row,9).value)
        fields['cg_lg_or_pc'] = tidy_and_decode(table10.cell(row,10).value)
        fields['nuts_region']  = clean_region(tidy_and_decode(table10.cell(row,11).value))
        fields['spending_04_05'] = tidy_and_decode(table10.cell(row,12).value)
        fields['spending_05_06'] = tidy_and_decode(table10.cell(row,13).value)
        fields['spending_06_07'] = tidy_and_decode(table10.cell(row,14).value)
        fields['spending_07_08'] = tidy_and_decode(table10.cell(row,15).value)
        fields['spending_08_09'] = tidy_and_decode(table10.cell(row,16).value)
        fields['spending_09_10'] = tidy_and_decode(table10.cell(row,17).value)
        entries10.append(fields)

    ###############################################
    # Compare each row & create lists
    # of matched and unmatched items.
    ###############################################
    log.info("Number in Table 9: %d", len(entries9))
    log.info("Number in Table 10: %d", len(entries10))

    joint_items = []
    unmatched_items_9 = list(entries9)
    unmatched_items_10 = list(entries10)

    for entry9 in entries9:
        for entry10 in entries10:
            if entry9['pog_alias'].lower()==entry10['pog_alias'].lower() \
            and entry9['cofog_1'].lower()==entry10['cofog_1'].lower() \
            and entry9['dept_name'].lower()==entry10['dept_name'].lower() \
            and entry9['spending_09_10']==entry10['spending_09_10'] \
            and entry9['spending_08_09']==entry10['spending_08_09'] \
            and entry9['spending_07_08']==entry10['spending_07_08'] \
            and entry9['spending_06_07']==entry10['spending_06_07'] \
            and entry9['spending_05_06']==entry10['spending_05_06'] \
            and entry9['spending_04_05']==entry10['spending_04_05'] \
            and entry9['nuts_region'][0:7]==entry10['nuts_region'][0:7]:
                joint_item = copy.deepcopy(entry9)
                joint_item['cofog_1'] = copy.deepcopy(entry10['cofog_1'])
                joint_item['hmt_1'] = copy.deepcopy(entry10['hmt_1'])
                joint_item['cofog_2'] = copy.deepcopy(entry10['cofog_2'])
                joint_item['hmt_2'] = copy.deepcopy(entry10['hmt_2'])
                joint_items.append(joint_item)
                unmatched_items_9.remove(entry9)
                unmatched_items_10.remove(entry10)
                entries10.remove(entry10)
                break

    for item in unmatched_items_9:
        item['cofog_2'] = "LA data sub_function"
        item['hmt_2'] = "LA data sub_function"
    for item in unmatched_items_10:
        item['spending_10_11'] = ""

    ###############################################
    # Take all the ENG_LA items from Table 9
    # and the ENG_HRA items with the POG mismatch.
    ###############################################
    temp_items = []
    for unmatched_item in unmatched_items_9:
        if unmatched_item['dept_name']=="ENG_LA" \
           or (unmatched_item['dept_name']=="ENG_HRA" and \
               unmatched_item['pog_alias']==\
               'LA dummy sprog 6. Housing and community amenities'):
            joint_items.append(unmatched_item)
        else:
            temp_items.append(unmatched_item)
    unmatched_items_9 = list(temp_items)

    del temp_items[:]
    for unmatched_item in unmatched_items_10:
        if unmatched_item['dept_name']!="ENG_LA" and \
           unmatched_item['pog_alias']!=\
            'LA dummy 6. Housing and community amenities':
            temp_items.append(unmatched_item)
    unmatched_items_10 = list(temp_items)

    log.info("Number of matched items found: %d", len(joint_items))
    log.info("Number unmatched from Table 9: %d", len(unmatched_items_9))
    log.info("Number unmatched from Table 10: %d", len(unmatched_items_10))

    # Check any remaining rows & fix by hand (I found 4 rows with typos).
    # The Treasury says that Table 10's spending figures are the ones to
    # use in the case of mismatches.

    #####################################
    # Write matched items to csv.
    #####################################
    cleancsv = csv.writer(out)

    cleancsv.writerow([
        'unique_id',
        'dept_code', 'dept_name',
        'cofog_level1_code', 'cofog_level1_name', 'wdmmg_cofog1_color',
        'cofog_level2_code', 'cofog_level2_name', 'wdmmg_cofog2_color',
        'cofog_level3_code', 'cofog_level3_name', 'wdmmg_cofog3_color',
        'hmt_functional', 'hmt_subfunctional',
        'pog', 'pog_alias',
        'id_or_non_id', 'cap_or_cur', 'cg_lg_or_pc', 'nuts_region',
        'tax_year',
        'amount'
    ])

    spending_years = ['04_05', '05_06', '06_07', '07_08', '08_09', '09_10', '10_11']

    for joint_item in joint_items:
        cofog_codes, cofog_names = cofog_from_hmt(joint_item['hmt_1'], joint_item['hmt_2'])

        for year in spending_years:
            tax_year = '20' + year[:2]
            source_amount = joint_item['spending_' + year]

            # Known bad values
            if source_amount in ['`']:
                log.warn("Found amount value '%s', converting to '0.0' to prevent errors. "
                         "Joint line:\n  %s", source_amount, joint_item)
                source_amount = '0.0'

            amount = 0 if source_amount == '' else AMOUNT_MULTIPLIER * float(source_amount)

            pog = joint_item['pog']
            pog_alias = joint_item['pog_alias']

            if pog_alias.startswith(pog + ' '):
                pog_alias = pog_alias[len(pog + ' '):]

            row = [
                uid_generator(tax_year),
                joint_item['dept_code'], joint_item['dept_name'],
                cofog_codes[0], cofog_names[0], wdmmg_color(cofog_codes[0]),
                cofog_codes[1], cofog_names[1], wdmmg_color(cofog_codes[1]),
                cofog_codes[2], cofog_names[2], wdmmg_color(cofog_codes[2]),
                joint_item['hmt_1'], joint_item['hmt_2'],
                pog, pog_alias,
                joint_item['id_or_non_id'], joint_item['cap_or_cur'],
                joint_item['cg_lg_or_pc'], joint_item['nuts_region'],
                tax_year, "%.2f" % amount
            ]

            cleancsv.writerow(row)

    #####################################
    # Write unmatched items to CSV.
    #####################################
    unmatched_9 = csv.writer(open('unmatched_table9.csv', 'wb'))
    unmatched_10 = csv.writer(open('unmatched_table10.csv', 'wb'))

    unmatched_9.writerow(['Dept Code', 'Dept Name', 'COFOG Level 1',
        'HMT Functional Classification', 'Programme Object Group',  \
        'Programme Object Group Alias', 'ID or non-ID', 'CAP or CUR', \
        'CG, LG or PC', 'NUTS 1 region', '2004-05', '2005-06', '2006-07', \
        '2007-08', '2008-09', '2009-10', '2010-11'])

    for unmatched_item in unmatched_items_9:
        row = [unmatched_item['dept_code'], unmatched_item['dept_name'],
               unmatched_item['cofog_1'], unmatched_item['hmt_1'],
               unmatched_item['pog'], unmatched_item['pog_alias'],
               unmatched_item['id_or_non_id'], unmatched_item['cap_or_cur'],
               unmatched_item['cg_lg_or_pc'], unmatched_item['nuts_region'],
               unmatched_item['spending_04_05'],
               unmatched_item['spending_05_06'],
               unmatched_item['spending_06_07'],
               unmatched_item['spending_07_08'],
               unmatched_item['spending_08_09'],
               unmatched_item['spending_09_10'],
               unmatched_item['spending_10_11']]
        unmatched_9.writerow(row)

    unmatched_10.writerow(['Dept Code', 'Dept Name', 'COFOG Level 1',
        'HMT Functional Classification', 'COFOG Level 2', \
        'HMT Sub-functional Classification', 'Programme Object Group',  \
        'Programme Object Group Alias', 'ID or non-ID', 'CAP or CUR', \
        'CG, LG or PC', 'NUTS 1 region', '2004-05', '2005-06', '2006-07', \
        '2007-08', '2008-09', '2009-10'])

    for entry in unmatched_items_10:
        row = [entry['dept_code'], entry['dept_name'], entry['cofog_1'],
               entry['hmt_1'], entry['cofog_2'], entry['hmt_2'], entry['pog'],
               entry['pog_alias'], entry['id_or_non_id'], entry['cap_or_cur'],
               entry['cg_lg_or_pc'], entry['nuts_region'],
               entry['spending_04_05'], entry['spending_05_06'],
               entry['spending_06_07'], entry['spending_07_08'],
               entry['spending_08_09'], entry['spending_09_10']]
        unmatched_10.writerow(row)
