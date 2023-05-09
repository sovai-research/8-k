import re
import time
from edgar import get_filings, set_identity
from datetime import datetime, timedelta
from config import sec_items, name, email, forms

set_identity(f"{name} {email}")


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

            # followed by a dot
            pattern = r"(\d+)\."
            replacement = r"\1. "
            text = text.replace(re.sub(pattern, replacement, item), item)

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
