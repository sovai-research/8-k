import re
import time
import os
import psycopg2
from edgar import get_filings, set_identity
from datetime import datetime, timedelta
from config import sec_items, name, email, forms
from contextlib import closing

set_identity(f"{name} {email}")
DRY_RUN = False


def conn_cur_decorator(func):
    """
    A method decorator to automatically close the database connection and cursor
    after the method has finished executing.
    """

    def wrapper(*args, **kwargs):
        dbname = os.environ.get("DBNAME")
        user = os.environ.get("DBUSER")
        password = os.environ.get("DBPASSWORD")
        host = os.environ.get("DBHOST")
        port = os.environ.get("DBPORT")

        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password,
            port=port,
        )
        with closing(conn), closing(conn.cursor()) as cur:
            result = func(cur, *args, **kwargs)
            conn.commit()
        return result

    return wrapper


@conn_cur_decorator
def save_company(cur, company_name, date, filing, sections):
    # check if a schema exists. if there is no schema, create one schema
    schema_name = "sec_reports"
    table_name = "eight_k"
    cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
    result = cur.fetchone()
    if result:
        print(f"The schema '{schema_name}' already exists.")
    else:
        cur.execute(f"CREATE SCHEMA {schema_name}")
        print(f"The schema '{schema_name}' has been created.")

    cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL, company_name VARCHAR(255), date DATE, filing VARCHAR(255), section_name VARCHAR(255), section_text TEXT,  PRIMARY KEY (company_name, date, filing, section_name) );")

    for section_name in sections:
        cur.execute(
            f"INSERT INTO {table_name} (company_name, date, filing, section_name, section_text) VALUES ('{company_name}', '{date}', '{filing}', '{section_name}', '{sections[section_name]}');")


def format_html(html):
    # Define regular expression pattern to remove HTML tags, newlines and HTML character entities
    html_pattern = re.compile(r"<.*?>")
    newline_pattern = re.compile(r"\n")
    character_entity_pattern = re.compile(r"&[#\w]+;")

    return re.sub(character_entity_pattern, "",
                  re.sub(html_pattern, "",
                         re.sub(newline_pattern, "", html)))


def get_yesterday_date():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y%m%d")


if __name__ == "__main__":
    # todo: move this to an endpoint or a more appropriate trigger point
    end_date = get_yesterday_date()
    start_date = end_date  # Change this value to the desired start date (e.g., "20230101")

    filings = get_filings(range(int(end_date), int(start_date)), form=forms)

    df = filings.to_pandas()
    df["url"] = "https://www.sec.gov/Archives/edgar/data/" + df["cik"].astype(str) + "/" + df[
        "accession_number"] + ".txt"
    df_8k = df[df["form"] == "8-K"]

    for i in range(len(filings)):
        start_time = time.time()
        url = df["url"][i]

        text = format_html(html=filings[i].html())
        text = ' '.join(text.split())
        # unique, weird to treat exceptions. all of them pertain to a certain entry
        # 2.03
        text = text.replace("Off-balance", "Off-Balance")
        text = text.replace("0ff-balance", "Off-Balance")
        text = text.replace("0ff-Balance", "Off-Balance")

        for item in [i for i in sec_items][:-1]:
            # normalise all cases with numbers in the beginning

            # Todo: this can surely be collapsed into fewer, smarter regular expressions.

            # todo: treat case of when there is a period (1.2.1.Words. instead of 1.2.1.Words etc) at the end of the
            #  item in a more general way
            text = text.replace(item[4:] + ".", item[4:])

            # todo: create the validator, do not store if data is invalid (i.e. more occurrences of the text after
            #  all non-letter characters have been removed are found) check for one whitespace
            pattern = sec_items[item]
            # r"(\d+\.\d+)([a-zA-Z])"
            # switch all this to translate
            """
            text = "This is a sample text with multiple occurrences of word1 and word2."

            # List of words to replace
            words_to_replace = ["word1", "word2"]

            # Replacement value
            replacement = "replacement_word"

            # Create translation table
            translation_table = str.maketrans({word: replacement for word in words_to_replace})

            # Perform replacements using translate
            new_text = text.translate(translation_table)

            print(new_text)
            """

            # treat for multiple whitespaces
            replacement = r"\1 \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1 \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1  \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1   \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1    \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1    \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1     \2"
            text = text.replace(re.sub(pattern, replacement, item), item)

            # treat for multiple whitespaces, followed by a dot
            replacement = r"\1.\2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1. \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1.  \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1.   \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1.    \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1.    \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1.     \2"
            text = text.replace(re.sub(pattern, replacement, item), item)

            # Dash
            replacement = r"\1-\2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1- \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1 - \2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            replacement = r"\1. -\2"
            text = text.replace(re.sub(pattern, replacement, item), item)
            ##
            ##
            # Different capitalisation

            # all lowercase:
            replacement = lambda m: m.group(1) + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + " " + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "  " + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "   " + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "." + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + ".  " + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + ".   " + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "  " + m.group(2).lower()
            text = text.replace(re.sub(pattern, replacement, item), item)

            # all uppercase:
            replacement = lambda m: m.group(1) + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + " " + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "  " + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "   " + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "." + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + ".  " + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + ".   " + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "  " + m.group(2).upper()
            text = text.replace(re.sub(pattern, replacement, item), item)
            # first letter of each word capitalised
            replacement = lambda m: m.group(1) + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + " " + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "  " + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "   " + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "." + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + ".  " + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + ".   " + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            replacement = lambda m: m.group(1) + "  " + m.group(2).title()
            text = text.replace(re.sub(pattern, replacement, item), item)

            ## todo: "Literary" Capitalisaitons: avoid prepositions, conjunctions, etc.
            # Depending to different popular styles.

            # todo: A lot of the erroneus entries have random lack of spaces (what I think happens is that
            #  they visually have a whitespace, but a different character in reality. test this hyp.)
            # words = item.split()
            # from itertools import combinations
            # [' '.join(words[j] + words[j + 1].replace(' ', '') if j in subset else words[j] for j in
            #           range(len(words) - 1)) + ' ' + words[-1] for r in range(len(words) - 1) for subset in
            #  combinations(range(len(words) - 1), r)]


        # normalise last case ("Signature"):
        signature_pattern = re.compile(r"(?i)signatures?")
        text = signature_pattern.sub("Signature", text)

        # compile all sec_items within a new regex
        sec_items_pattern = "|".join(sec_items)
        # get all matches within the modified text
        sec_items_matches = re.findall(sec_items_pattern, text)

        sec_items_data = {}
        current_item = ""
        current_text = ""

        for match in sec_items_matches:
            # check new match against current item
            if match != current_item:
                # when a new item has been found, store the previous one and start the new one
                if current_item != "":
                    sec_items_data[current_item] = current_text.strip()
                current_item = match
                current_text = ""
            current_text += text.split(match, 1)[1]

        # store last
        if current_item != "":
            sec_items_data[current_item] = current_text.strip()

        company_time = time.time() - start_time

        print(f"Company: {df['company'][i]}")
        print(f"Duration: {company_time:.5f} seconds")
        print(f"Items found: {len(sec_items_data)}: {[item for item in sec_items_data]}")
        save = True
        for j in sec_items:
            if j.lower().replace(" ", "").replace(".", "").replace("-", "") in text.lower().replace(" ", "").replace(
                    ".", "").replace("-", "") and j not in sec_items_data:
                # file_path = 'test_file_8k.csv'
                # Define the data to be written as a new line
                # new_line = [df["company"][i], df["url"][i], df["cik"][i], df["filing_date"][i], j]

                # Open the file in append mode
                # import csv

                # with open(file_path, 'a', newline='') as csv_file:
                #    writer = csv.writer(csv_file)

                #    # Write the new line to the file
                #    writer.writerow(new_line)

                # Close the file
                # csv_file.close()
                save = False
        if not DRY_RUN and save:
            # company name, date, filing, section name, text
            # todo: the code below is not very Pythonic, but easier to read imo. Modify when the requirements are fully cristalised and provide clarity through better comments
            company_name = df["company"][i]
            # convert dates to a format Postgres can digest
            date = df["filing_date"][i].strftime('%Y-%m-%d %H:%M:%S.%f')
            filing = df["form"][i]

            # section_name is the key, text is the value
            sections = sec_items_data
            save_company(company_name=company_name, date=date, filing=filing, sections=sections)
