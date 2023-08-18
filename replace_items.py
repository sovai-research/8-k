import re
def replace_item_1_01(text):
    pattern = r'1\.01[.,;]?\s*Entry\s*into\s*[.,;]?\s*a\s*[.,;]?\s*Material\s*[.,;]?\s*Definitive\s*[.,;]?\s*Agreement'
    return re.sub(pattern, '1.01Entry into a Material Definitive Agreement', text, flags=re.IGNORECASE)

def replace_item_1_02(text):
    pattern = r'1\.02[.,;]?\s*Termination\s*of\s*[.,;]?\s*a\s*[.,;]?\s*Material\s*[.,;]?\s*Definitive\s*[.,;]?\s*Agreement'
    return re.sub(pattern, '1.02Termination of a Material Definitive Agreement', text, flags=re.IGNORECASE)

def replace_item_1_03(text):
    pattern = r'1\.03[.,;]?\s*Bankruptcy\s*[.,;]?\s*or\s*[.,;]?\s*Receivership'
    return re.sub(pattern, '1.03Bankruptcy or Receivership', text, flags=re.IGNORECASE)


def replace_item_1_04(text):
    pattern = r'1\.04[.,;]?\s*Mine\s*[.,;]?\s*Safety\s*[.,;]?\s*-\s*[.,;]?\s*Reporting\s*[.,;]?\s*of\s*[.,;]?\s*Shutdowns\s*[.,;]?\s*and\s*[.,;]?\s*Patterns\s*[.,;]?\s*of\s*[.,;]?\s*Violations'
    return re.sub(pattern, '1.04Mine Safety - Reporting of Shutdowns and Patterns of Violations', text,
                  flags=re.IGNORECASE)


def replace_item_2_01(text):
    pattern = r'2\.01[.,;]?\s*Completion\s*[.,;]?\s*of\s*[.,;]?\s*Acquisition\s*[.,;]?\s*or\s*[.,;]?\s*Disposition\s*[.,;]?\s*of\s*[.,;]?\s*Assets'
    return re.sub(pattern, '2.01Completion of Acquisition or Disposition of Assets', text, flags=re.IGNORECASE)


def replace_item_2_02(text):
    # good one is first
    pattern = r'2\.02[.,;]?\s*Results\s*[.,;]?\s*of\s*[.,;]?\s*Operations\s*[.,;]?\s*and\s*[.,;]?\s*Financial\s*[.,;]?\s*Condition'
    return re.sub(pattern, '2.02Results of Operations and Financial Condition', text, flags=re.IGNORECASE)


def replace_item_2_03(text):
    pattern = r'2\.03[.,;]?\s*Creation\s*[.,;]?\s*of\s*[.,;]?\s*a\s*[.,;]?\s*Direct\s*[.,;]?\s*Financial\s*[.,;]?\s*Obligation\s*[.,;]?\s*or\s*[.,;]?\s*an\s*[.,;]?\s*Obligation\s*[.,;]?\s*under\s*[.,;]?\s*an\s*[.,;]?\s*Off-Balance\s*[.,;]?\s*Sheet\s*[.,;]?\s*Arrangement\s*[.,;]?\s*of\s*[.,;]?\s*a\s*[.,;]?\s*Registrant'
    return re.sub(pattern,
                  '2.03Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant',
                  text, flags=re.IGNORECASE)


def replace_item_2_04(text):
    pattern = r'2\.04[.,;]?\s*Triggering\s*[.,;]?\s*Events\s*[.,;]?\s*That\s*[.,;]?\s*Accelerate\s*[.,;]?\s*or\s*[.,;]?\s*Increase\s*[.,;]?\s*a\s*[.,;]?\s*Direct\s*[.,;]?\s*Financial\s*[.,;]?\s*Obligation\s*[.,;]?\s*or\s*[.,;]?\s*an\s*[.,;]?\s*Obligation\s*[.,;]?\s*under\s*[.,;]?\s*an\s*[.,;]?\s*Off-Balance\s*[.,;]?\s*Sheet\s*[.,;]?\s*Arrangement'
    return re.sub(pattern,
                  '2.04Triggering Events That Accelerate or Increase a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement',
                  text, flags=re.IGNORECASE)


def replace_item_2_05(text):
    pattern = r'2\.05[.,;]?\s*Costs\s*[.,;]?\s*Associated\s*[.,;]?\s*with\s*[.,;]?\s*Exit\s*[.,;]?\s*or\s*[.,;]?\s*Disposal\s*[.,;]?\s*Activities'
    return re.sub(pattern, '2.05Costs Associated with Exit or Disposal Activities', text, flags=re.IGNORECASE)


def replace_item_2_06(text):
    pattern = r'2\.06[.,;]?\s*Material\s*[.,;]?\s*Impairments'
    return re.sub(pattern, '2.06Material Impairments', text, flags=re.IGNORECASE)


def replace_item_3_01(text):
    pattern = r'3\.01[.,;]?\s*Notice\s*[.,;]?\s*of\s*[.,;]?\s*Delisting\s*[.,;]?\s*or\s*[.,;]?\s*Failure\s*[.,;]?\s*to\s*[.,;]?\s*Satisfy\s*[.,;]?\s*a\s*[.,;]?\s*Continued\s*[.,;]?\s*Listing\s*[.,;]?\s*Rule\s*[.,;]?\s*or\s*[.,;]?\s*Standard\s*[.,;]?\s*;\s*[.,;]?\s*Transfer\s*[.,;]?\s*of\s*[.,;]?\s*Listing'
    return re.sub(pattern,
                  '3.01Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing',
                  text, flags=re.IGNORECASE)


def replace_item_3_02(text):
    pattern = r'3\.02[.,;]?\s*Unregistered\s*[.,;]?\s*Sales\s*[.,;]?\s*of\s*[.,;]?\s*Equity\s*[.,;]?\s*Securities'
    return re.sub(pattern, '3.02Unregistered Sales of Equity Securities', text, flags=re.IGNORECASE)


def replace_item_3_03(text):
    pattern = r'3\.03[.,;]?\s*Material\s*[.,;]?\s*Modifications\s*[.,;]?\s*to\s*[.,;]?\s*Rights\s*[.,;]?\s*of\s*[.,;]?\s*Security\s*[.,;]?\s*Holders'
    return re.sub(pattern, '3.03Material Modifications to Rights of Security Holders', text, flags=re.IGNORECASE)


def replace_item_4_01(text):
    pattern = r'4\.01[.,;]?\s*Changes\s*[.,;]?\s*in\s*[.,;]?\s*Registrant\s*[.,;]?\s*s\s*[.,;]?\s*Certifying\s*[.,;]?\s*Accountant'
    return re.sub(pattern, '4.01Changes in Registrant\'s Certifying Accountant', text, flags=re.IGNORECASE)


def replace_item_4_02(text):
    pattern = r'4\.02[.,;]?\s*Non-Reliance\s*[.,;]?\s*on\s*[.,;]?\s*Previously\s*[.,;]?\s*Issued\s*[.,;]?\s*Financial\s*[.,;]?\s*Statements\s*[.,;]?\s*or\s*[.,;]?\s*a\s*[.,;]?\s*Related\s*[.,;]?\s*Audit\s*[.,;]?\s*Report\s*[.,;]?\s*or\s*[.,;]?\s*Completed\s*[.,;]?\s*Interim\s*[.,;]?\s*Review'
    return re.sub(pattern,
                  '4.02Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim Review',
                  text, flags=re.IGNORECASE)


def replace_item_5_01(text):
    pattern = r'5\.01[.,;]?\s*Changes\s*[.,;]?\s*in\s*[.,;]?\s*Control\s*[.,;]?\s*of\s*[.,;]?\s*Registrant'
    return re.sub(pattern, '5.01Changes in Control of Registrant', text, flags=re.IGNORECASE)


def replace_item_5_02(text):
    pattern = r'5\.02[.,;]?\s*Departure\s*[.,;]?\s*of\s*[.,;]?\s*Directors\s*[.,;]?\s*or\s*[.,;]?\s*Certain\s*[.,;]?\s*Officers\s*[.,;]?\s*;\s*[.,;]?\s*Election\s*[.,;]?\s*of\s*[.,;]?\s*Directors\s*[.,;]?\s*;\s*[.,;]?\s*Appointment\s*[.,;]?\s*of\s*[.,;]?\s*Certain\s*[.,;]?\s*Officers\s*[.,;]?\s*;\s*[.,;]?\s*Compensatory\s*[.,;]?\s*Arrangements\s*[.,;]?\s*of\s*[.,;]?\s*Certain\s*[.,;]?\s*Officers'
    return re.sub(pattern,
                  '5.02Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers',
                  text, flags=re.IGNORECASE)


def replace_item_5_03(text):
    pattern = r'5\.03[.,;]?\s*Amendments\s*[.,;]?\s*to\s*[.,;]?\s*Articles\s*[.,;]?\s*of\s*[.,;]?\s*Incorporation\s*[.,;]?\s*or\s*[.,;]?\s*Bylaws\s*[.,;]?\s*;\s*[.,;]?\s*Change\s*[.,;]?\s*in\s*[.,;]?\s*Fiscal\s*[.,;]?\s*Year'
    return re.sub(pattern, '5.03Amendments to Articles of Incorporation or Bylaws; Change in Fiscal Year', text,
                  flags=re.IGNORECASE)


def replace_item_5_04(text):
    pattern = r'5\.04[.,;]?\s*Temporary\s*[.,;]?\s*Suspension\s*[.,;]?\s*of\s*[.,;]?\s*Trading\s*[.,;]?\s*Under\s*[.,;]?\s*Registrant\s*[.,;]?\s*s\s*[.,;]?\s*Employee\s*[.,;]?\s*Benefit\s*[.,;]?\s*Plans'
    return re.sub(pattern, '5.04Temporary Suspension of Trading Under Registrant\'s Employee Benefit Plans', text,
                  flags=re.IGNORECASE)


def replace_item_5_05(text):
    pattern = r'5\.05[.,;]?\s*Amendments\s*[.,;]?\s*to\s*[.,;]?\s*the\s*[.,;]?\s*Registrant\s*[.,;]?\s*s\s*[.,;]?\s*Code\s*[.,;]?\s*of\s*[.,;]?\s*Ethics\s*[.,;]?\s*,\s*[.,;]?\s*or\s*[.,;]?\s*Waiver\s*[.,;]?\s*of\s*[.,;]?\s*a\s*[.,;]?\s*Provision\s*[.,;]?\s*of\s*[.,;]?\s*the\s*[.,;]?\s*Code\s*[.,;]?\s*of\s*[.,;]?\s*Ethics'
    return re.sub(pattern,
                  '5.05Amendments to the Registrant\'s Code of Ethics, or Waiver of a Provision of the Code of Ethics',
                  text, flags=re.IGNORECASE)


def replace_item_5_06(text):
    pattern = r'5\.06[.,;]?\s*Change\s*[.,;]?\s*in\s*[.,;]?\s*Shell\s*[.,;]?\s*Company\s*[.,;]?\s*Status'
    return re.sub(pattern, '5.06Change in Shell Company Status', text, flags=re.IGNORECASE)


def replace_item_5_07(text):
    pattern = r'5\.07[.,;]?\s*Submission\s*[.,;]?\s*of\s*[.,;]?\s*Matters\s*[.,;]?\s*to\s*[.,;]?\s*a\s*[.,;]?\s*Vote\s*[.,;]?\s*of\s*[.,;]?\s*Security\s*[.,;]?\s*Holders'
    return re.sub(pattern, '5.07Submission of Matters to a Vote of Security Holders', text, flags=re.IGNORECASE)


def replace_item_5_08(text):
    pattern = r'5\.08[.,;]?\s*Shareholder\s*[.,;]?\s*Director\s*[.,;]?\s*Nominations'
    return re.sub(pattern, '5.08Shareholder Director Nominations', text, flags=re.IGNORECASE)


def replace_item_6_01(text):
    pattern = r'6\.01[.,;]?\s*ABS\s*[.,;]?\s*Informational\s*[.,;]?\s*and\s*[.,;]?\s*Computational\s*[.,;]?\s*Material'
    return re.sub(pattern, '6.01ABS Informational and Computational Material', text, flags=re.IGNORECASE)


def replace_item_6_02(text):
    pattern = r'6\.02[.,;]?\s*Change\s*[.,;]?\s*of\s*[.,;]?\s*Servicer\s*[.,;]?\s*or\s*[.,;]?\s*Trustee'
    return re.sub(pattern, '6.02Change of Servicer or Trustee', text, flags=re.IGNORECASE)


def replace_item_6_03(text):
    pattern = r'6\.03[.,;]?\s*Change\s*[.,;]?\s*in\s*[.,;]?\s*Credit\s*[.,;]?\s*Enhancement\s*[.,;]?\s*or\s*[.,;]?\s*Other\s*[.,;]?\s*External\s*[.,;]?\s*Support'
    return re.sub(pattern, '6.03Change in Credit Enhancement or Other External Support', text, flags=re.IGNORECASE)


def replace_item_6_04(text):
    pattern = r'6\.04[.,;]?\s*Failure\s*[.,;]?\s*to\s*[.,;]?\s*Make\s*[.,;]?\s*a\s*[.,;]?\s*Required\s*[.,;]?\s*Distribution\s*[.,;]?\s*or\s*[.,;]?\s*Payment'
    return re.sub(pattern, '6.04Failure to Make a Required Distribution or Payment', text, flags=re.IGNORECASE)


def replace_item_6_05(text):
    pattern = r'6\.05[.,;]?\s*Securities\s*[.,;]?\s*Act\s*[.,;]?\s*Updating\s*[.,;]?\s*Disclosure'
    return re.sub(pattern, '6.05Securities Act Updating Disclosure', text, flags=re.IGNORECASE)


def replace_item_6_06(text):
    pattern = r'6\.06[.,;]?\s*Static\s*[.,;]?\s*Pool'
    return re.sub(pattern, '6.06Static Pool', text, flags=re.IGNORECASE)


def replace_item_6_08(text):
    pattern = r'6\.08[.,;]?\s*Change\s*[.,;]?\s*To\s*[.,;]?\s*Security\s*[.,;]?\s*Classes\s*[.,;]?\s*or\s*[.,;]?\s*Payment\s*[.,;]?\s*Terms'
    return re.sub(pattern, '6.08Change To Security Classes or Payment Terms', text, flags=re.IGNORECASE)


def replace_item_6_10(text):
    pattern = r'6\.10[.,;]?\s*Alternative\s*[.,;]?\s*Filings\s*[.,;]?\s*of\s*[.,;]?\s*Asset-Backed\s*[.,;]?\s*Issuers'
    return re.sub(pattern, '6.10Alternative Filings of Asset-Backed Issuers', text, flags=re.IGNORECASE)


def replace_item_7_01(text):
    pattern = r'7\.01[.,;]?\s*Regulation\s*[.,;]?\s*FD\s*[.,;]?\s*Disclosure'
    return re.sub(pattern, '7.01Regulation FD Disclosure', text, flags=re.IGNORECASE)


def replace_item_8_01(text):
    pattern = r'8\.01[.,;]?\s*Other\s*[.,;]?\s*Events'
    return re.sub(pattern, '8.01Other Events', text, flags=re.IGNORECASE)


def replace_item_9_01(text):
    pattern = r'9\.01[.,;]?\s*Financial\s*[.,;]?\s*Statements\s*[.,;]?\s*and\s*[.,;]?\s*Exhibits'
    return re.sub(pattern, '9.01Financial Statements and Exhibits', text, flags=re.IGNORECASE)


def replace_all_items(text):
    text = replace_item_1_01(text)
    text = replace_item_1_02(text)
    text = replace_item_2_02(text)
    text = replace_item_2_03(text)
    text = replace_item_2_04(text)
    text = replace_item_2_05(text)
    text = replace_item_2_06(text)
    text = replace_item_3_01(text)
    text = replace_item_3_02(text)
    text = replace_item_3_03(text)
    text = replace_item_4_01(text)
    text = replace_item_4_02(text)
    text = replace_item_5_01(text)
    text = replace_item_5_02(text)
    text = replace_item_5_03(text)
    text = replace_item_5_04(text)
    text = replace_item_5_05(text)
    text = replace_item_5_06(text)
    text = replace_item_5_07(text)
    text = replace_item_5_08(text)
    text = replace_item_6_01(text)
    text = replace_item_6_02(text)
    text = replace_item_6_03(text)
    text = replace_item_6_04(text)
    text = replace_item_6_05(text)
    text = replace_item_6_06(text)
    text = replace_item_6_10(text)
    text = replace_item_7_01(text)
    text = replace_item_8_01(text)
    text = replace_item_9_01(text)
    return text
