import sys
from datetime import datetime
import time
import traceback
import json
import os
# How do I add the below to the venv path?
sys.path.append("/home/joey/bird_mail/ebird")
sys.path.append("/home/joey/bird_mail/gmail")
from EBirdWrapper import EBirdWrapper
from GmailWrapper import GmailWrapper

if __name__ == "__main__":
    # Set file path
    SERVICE_FILE_PATH = os.path.realpath(__file__).replace(os.path.realpath(__file__).split("/")[-1], "")
    # Read eBird token
    token_path = SERVICE_FILE_PATH + "ebird_token.txt"
    with open(token_path, "r") as f:
        TOKEN = f.read()
    # Create wrapper objects
    e_bird_obj  = EBirdWrapper(TOKEN)
    gmail_obj   = GmailWrapper()
    # Time to get data
    region_code     = "US-CA-037"
    # species_code    = "mallar3"
    back            = 1
    max_results     = 5
    last_obs_id     = ""
    to_addr         = "joseph.girardini@gmail.com"
    gmail_result = ""
    # Load mailing list
    with open(SERVICE_FILE_PATH + "mailing_list.json", "r") as f:
        mailing_list = json.loads(f.read())
    while True:
        try:
            # Loop through mailing list, make map of data to be sent
            result_map = {}
            results = []
            num = 1
            for species_code in mailing_list:
                results = e_bird_obj.get_species_info_for_region(region_code, species_code, back=back, max_results=max_results)
                for email in mailing_list[species_code]:
                    if result_map.get(email) == None:
                        result_map[email] = [*results]
                    else:
                        result_map[email] += results
            # Loop through data map, send emails
            for email in result_map:
                content = ""
                for result in result_map[email]:
                    content += f"++++++++++++++ {result['comName']} ++++++++++++++\n"
                    # Check for new observation; if new one, update last id and send email
                    if result is not None and result["subId"] != last_obs_id:
                        last_obs_id = result["subId"]
                        for field in result:
                            content += field + " : " + str(result[field]) + "\n"
                        content += "\n"
                subject = datetime.fromtimestamp(time.time()).strftime('Bird data on %m/%d/%Y at %H:%M')
                gmail_result = gmail_obj.send_gmail_message(content, to_addr, subject)
                print(f"Gmail sent:\n{gmail_result}")
            # Poll every day lol
            time.sleep(60*60*24)
        except Exception:
            print("got exception")
            print(traceback.format_exc())
            with open("error.txt", "w") as f:
                f.write(traceback.format_exc())
            exit(1)
