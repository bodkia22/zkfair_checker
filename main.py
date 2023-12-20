import requests
import json
import pandas as pd

BASE_URL = "https://api.zkfair.io/data/api/community-airdrop"

with open("addresses.txt", "r") as file:
    addresses = file.readlines()

addresses = [address.strip() for address in addresses if address.strip()]


def getUrlWithWallet(address):
    return f"{BASE_URL}?address={address}"


all_formatted_data = []

for address in addresses:
    url_w = getUrlWithWallet(address)
    print(f"Processing address: {address}")

    response = requests.get(url_w)
    print(response.status_code)
    print(response.text)
    print("-" * 50)

    data = json.loads(response.text)
    airdrop_data = data["community_airdrop"]

    formatted_data = {
        "addr": address,
        **{
            key: float(value["value_decimal"])
            if value["value_decimal"] != "0E-18"
            else 0
            for key, value in airdrop_data.items()
        },
    }

    all_formatted_data.append(formatted_data)

df = pd.DataFrame(all_formatted_data)
df.to_excel("output.xlsx", index=False, engine="openpyxl")
print("Data saved to output.xlsx")
