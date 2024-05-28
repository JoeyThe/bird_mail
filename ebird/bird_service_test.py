from EBirdWrapper import EBirdWrapper
import time
import json

test = EBirdWrapper("2fkoo1rimpng")

# with open("ebird_taxonomy.csv", "w") as f:
#     f.write(test.get_ebird_taxonomy())

# print(test.get_species_info_for_region("US-MA-019", "mallar3", back=1, maxResults=1), end="\n\n")
for obs in test.get_species_info_for_region("US-AZ", "gamqua", maxResults=1000):
    if "Sedona" in obs['locName']:
        print(obs)

# with open("region_codes.json", "w") as f:
#     region_dict = {}
#     for state in state_codes:
#         time.sleep(1)
#         region_dict[state] = {}
#         for region in test.getRegionInfo(f"{state}"):
#             try:
#                 region_dict[state][region['name']] = region['code']
#             except:
#                 print("BAD STATE")
#     json.dump(region_dict, f)
