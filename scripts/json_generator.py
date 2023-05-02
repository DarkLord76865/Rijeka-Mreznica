import json
from json_loader import load_json

info = load_json("../data/mreznica.json")

for i in info["Mrežnica"]["lokacije"]["slapovi"].keys():
	info["Mrežnica"]["lokacije"]["slapovi"][i]["udaljenost do ušća"] = round(info["Mrežnica"]["duljina"] - info["Mrežnica"]["lokacije"]["slapovi"][i]["udaljenost do izvora"], 2)

with open("../data/mreznica.json", "w", encoding="utf-8") as file:
	json.dump(info, file, indent=4, ensure_ascii=False)


# for i in info["Mrežnica"]["lokacije"]["slapovi"].keys():
# 	info["Mrežnica"]["lokacije"]["slapovi"][i]["vrsta"] = "slap"
# 	info["Mrežnica"]["lokacije"]["slapovi"][i]["visina"] = 1.0
# 	info["Mrežnica"]["lokacije"]["slapovi"][i]["udaljenost do izvora"] = 0

# info = {"Mrežnica": {
# 	"duljina": 64,
# 	"izvor": "",
# 	"ušće": "",
# 	"opis": "",
# 	"lokacije": {
# 		"izvor": {},
# 		"ušće": {},
# 		"slapovi": {},
# 	}
# 	}
# }
#
# for i in range(1, 93):
# 	info["Mrežnica"]["lokacije"]["slapovi"][f"{i}"] = {
# 		"ime": "",
# 		"vrsta": "",
# 		"visina": "",
# 		"udaljenost do izvora": 64,
# 		"udaljenost do ušća": 64,
# 		"opis": ""
# 	}
