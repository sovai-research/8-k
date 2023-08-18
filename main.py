import re
import csv
import os
import psycopg2
from fastapi import FastAPI, HTTPException
from edgar import get_filings, set_identity
from datetime import datetime, timedelta
from config import sec_items, name, email, forms
from contextlib import closing
from replace_items import replace_all_items

set_identity(f"{name} {email}")
DRY_RUN = False
app = FastAPI(debug=True)


# Master function to replace all items in the given text

###########

def replace_variations(text):
    items = [i for i in sec_items]
    for item in items[:-1]:
        number, rest_of_item = item.split(' ', 1)  # Split the item into number and the rest of the text
        number_pattern = re.escape(number)  # Escape any special characters in the number part
        rest_pattern = rest_of_item.replace(' ',
                                            r'[ \-]{0,15}')  # Replace spaces with a pattern that matches 0 to 15
        # spaces or hyphens
        for word in re.findall(r'\w+', rest_pattern):  # Iterate through each word found in the rest pattern
            # Replace the word in the pattern with the word itself followed by optional plural suffixes (s/es)
            rest_pattern = rest_pattern.replace(word, f'{word}[s]?[es]?')
        # Create the final pattern by combining the number pattern and the rest pattern, allowing for 0 to 1 space or
        # hyphen in between
        pattern = f'{number_pattern}[ \-]?{rest_pattern}'
        # Replace occurrences of the pattern in the text with the original item, ignoring the case
        text = re.sub(pattern, item, text, flags=re.IGNORECASE)

    return text


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
        f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (id SERIAL, company_name VARCHAR(255), date DATE, filing VARCHAR(255), section_name VARCHAR(255), section_text TEXT,  PRIMARY KEY (company_name, date, filing, section_name) );")
    for section_name in sections:
        cur.execute(
            f"INSERT INTO {table_name} (company_name, date, filing, section_name, section_text) VALUES ('{company_name}', '{date}', '{filing}', '{section_name}', '{sections[section_name]}');")

def format_html(html):
    # Define regular expression pattern to remove HTML tags, newlines and HTML character entities
    html_pattern = re.compile(r"<.*?>")
    newline_pattern = re.compile(r"\n")
    character_entity_pattern = re.compile(r"&[#\w]+;")
    backlash_t = re.compile(r"\t")
    return re.sub(backlash_t, "",
                  re.sub(character_entity_pattern, "", re.sub(html_pattern, "", re.sub(newline_pattern, "", html))))


def get_yesterday_date():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y%m%d")


def parse_date(date_str):
    formats = [
        "%Y-%m-%d %H:%M:%S.%f",  # with time and milliseconds
        "%Y-%m-%d %H:%M:%S",  # with time
        "%Y-%m-%d"  # without time
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Date string {date_str} does not match any known formats")

@app.post('/filings_between_periods')
def store_filings_between_periods(start_date: str, end_date: str):
    # discuss format for start_date/end_date
    start_date, end_date = parse_date(start_date), parse_date(end_date)
    process_filings(start_date, end_date)

    return {"Status": "200"}  # todo: convert to a proper response. add some data about what was saved.


def process_filings(start_date, end_date):
    # date needs to be converted to timestamp. casting it to integer due to some weird interaction with decimals.
    filings = get_filings(range(int(end_date.timestamp()), int(start_date.timestamp())), form=forms)

    df = filings.to_pandas()
    df["url"] = "https://www.sec.gov/Archives/edgar/data/" + df["cik"].astype(str) + "/" + df[
        "accession_number"] + ".txt"
    correct_counter = 0
    wrong_counter = 0
    for i in range(len(filings)):

        text = format_html(html=filings[i].html())

        text = replace_all_items(text)

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

        correct = True
        for j in sec_items:
            if j.lower().replace(" ", "").replace(".", "").replace("-", "") in text.lower().replace(" ", "").replace(
                    ".", "").replace("-", "") and j not in sec_items_data:
                file_path = '/Users/filipbriac/upwork/DerekSnow/8-k/test_file_8k.csv'
                # Define the data to be written as a new line
                correct = False
                # here to save
                new_line = [df["cik"][i], j]
                # Open the file in append mode

                with open(file_path, 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)

                    # Write the new line to the file
                    writer.writerow(new_line)

                # Close the file
                csv_file.close()
        if correct:
            correct_counter += 1
        else:
            wrong_counter += 1
        if (wrong_counter + correct_counter) % 100 == 0:
            print(f"Wrong: {wrong_counter}/{wrong_counter + correct_counter}")
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


if __name__ == "__main__":
    process_filings(start_date=parse_date("2023-01-12"), end_date=parse_date("2023-01-14"))
    # %Y-%m-%d
