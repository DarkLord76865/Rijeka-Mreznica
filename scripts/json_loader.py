import json


def load_json(file_path):

	with open(file_path, "r", encoding="utf-8") as file:
		info = json.load(file)

	return info


if __name__ == "__main__":
	print(load_json("../data/mreznica.json"))
