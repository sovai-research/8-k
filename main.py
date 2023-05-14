import re
import time
import os
import psycopg2
from edgar import get_filings, set_identity
from datetime import datetime, timedelta
from config import sec_items, name, email, forms
from contextlib import closing

set_identity(f"{name} {email}")
DRY_RUN = True

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

    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL, company_name VARCHAR(255), date DATE, filing VARCHAR(255), section_name VARCHAR(255), section_text TEXT,  PRIMARY KEY (company_name, date, filing, section_name) );")
    for section_name in sections:
        cur.execute(f"INSERT INTO {table_name} (company_name, date, filing, section_name, section_text) VALUES ('{company_name}', '{date}', '{filing}', '{section_name}', '{sections[section_name]}');")


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
    df["url"] = "https://www.sec.gov/Archives/edgar/data/" + df["cik"].astype(str) + "/" + df["accession_number"] + ".txt"
    df_8k = df[df["form"] == "8-K"]

    for i in range(len(filings)):
        start_time = time.time()
        url = df["url"][i]

        text = format_html(html=filings[i].html())

        for item in sec_items[:-1]:
            # normalise all cases with numbers in the beginning

            # Todo: this can surely be collapsed into fewer, smarter regular expressions.


            # todo: treat case of when there is a period (1.2.1.Words. instead of 1.2.1.Words etc) at the end of the item in a more general way
            text = text.replace(item[4:] + ".", item[4:])


            # todo: create the validator, do not store if data is invalid (i.e. more occurrences of the text after all non-letter characters have been removed are found)
            # check for one whitespace
            pattern = r"(\d+\.\d+)([a-zA-Z])"
            replacement = r"\1 \2"
            text = text.replace(re.sub(pattern, replacement, item), item)

            # check for multiple whitespaces
            pattern = r"(\d+\.\d+)\s+(.*)"
            replacement = r"\1 \2"
            text = text.replace(re.sub(pattern, replacement, item), item)

            # followed by whitespace and dots
            pattern = r"^(\d+\.\d+)(\D.*)$"
            replacement = r"\1. \2"
            text = text.replace(re.sub(pattern, replacement, item), item)

            # followed by a dot. This is currently causing problems, fix in progress.
            pattern = r"\d+\.\d+\.[a-zA-Z]+"
            replacement = r"\1. \2"
            # todo: modify below case to catch
            # text = text.replace(re.sub(pattern, replacement, item), item)

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
        if not DRY_RUN:
            # company name, date, filing, section name, text
            # todo: the code below is not very Pythonic, but easier to read imo. Modify when the requirements are fully cristalised and provide clarity through better comments
            company_name = df["company"][i]
            # convert dates to a format Postgres can digest
            date = df["filing_date"][i].strftime('%Y-%m-%d %H:%M:%S.%f')
            filing = df["form"][i]

            # section_name is the key, text is the value
            sections = sec_items_data
            save_company(company_name=company_name, date=date, filing=filing, sections=sections)


