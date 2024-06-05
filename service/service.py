import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from collections import defaultdict
# We'll fix thisP
from EBirdWrapper import EBirdWrapper
from GmailWrapper import GmailWrapper


REGION_CODE = "US-CA-037"

if __name__ == "__main__":
    # Let's update this
    SERVICE_FILE_PATH = os.path.realpath(__file__).replace(os.path.realpath(__file__).split("/")[-1], "")

    # Read eBird token
    token_path = SERVICE_FILE_PATH + "ebird_token.txt"

    with open(token_path, "r") as f:
        TOKEN = f.read()

    # Create wrapper objects
    e_bird_obj = EBirdWrapper(TOKEN)
    gmail_obj = GmailWrapper()

    # Time to get data
    region_code = "US-CA-037"

    # Let's make these args or something ..
    back = 1
    max_results = 5
    last_obs_id = ""
    to_addr = "joseph.girardini@gmail.com"
    gmail_result = ""

    # Load mailing list
    with open(SERVICE_FILE_PATH + "mailing_list.json", "r") as f:
        mailing_list = json.loads(f.read())

    while True:
        try:
            # Loop through mailing list, make map of data to be sent
            result_map = defaultdict(list)
            results = []
            num = 1

            for species_code, emails in mailing_list.items():

                results = e_bird_obj.get_species_info_for_region(
                    region_code,
                    species_code,
                    back=back,
                    max_results=max_results,
                )

                for email in emails:
                    results[email] += results

            # Loop through data map, send emails
            for email in result_map:
                content = ""
                for result in result_map[email]:
                    content += f"++++++++++++++ {result['comName']} ++++++++++++++\n"
                    # Check for new observation; if new one, update last id and send email
                    if result["subId"] != last_obs_id:
                        last_obs_id = result["subId"]
                        for field in result:
                            content += field + " : " + str(result[field]) + "\n"
                        content += "\n"
                subject = f"Bird data on {datetime.now(timezone.utc).isoformat()}"
                gmail_result = gmail_obj.send_gmail_message(content, to_addr, subject)
                print(f"Gmail sent:\n{gmail_result}")
            # Make this a cron ...
            time.sleep(60 * 60 * 24)
        except Exception:
            print("got exception")
            print(traceback.format_exc())
            with open("error.txt", "w") as f:
                f.write(traceback.format_exc())
            exit(1)
