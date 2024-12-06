import json
from collections import defaultdict
from tqdm import tqdm

from company import Company
from parse_json import process_company_entry


# missing, duplicates, corrections

# Total: 878 After filteration: 675
# Number of missing company names: 203
# Number of duplicates found: 1


if __name__ == "__main__":
    input_file = "../data/company_data.json"
    input_file_cleaned = "../data/cleaned_company_data.json"

    with open(input_file, "r", encoding="utf-8") as fin1:
        raw_data = json.load(fin1)

    # with open(input_file_cleaned, "r", encoding="utf-8") as fin2:
    #     cleaned_data = json.load(fin2)

    simple_set = set()
    company_stats = defaultdict(int)

    empty_name = 0
    processed_data = []
    for id, company in enumerate(tqdm(raw_data)):
        company = Company(company)
        company['id'] = id

        simple_set.add(company)

        if company['name'] is None:
            empty_name += 1

        if company['name'] is not None:
            processed_entry = process_company_entry(company, get_text_blocks=False)
            processed_data.append(processed_entry)

            company_stats[(company.get("name"), company.get("website"), company.get("year_of_founding"))] += 1

    print("Total:", len(processed_data) + empty_name, "After filteration:", len(processed_data))
    print("Number of missing company names:", empty_name)
    print("Number of duplicates found:", len(simple_set) - len(processed_data))

    # print(sorted(company_stats.items(), key=lambda item: item[1], reverse=True)[:10])
    processed_data = list(set(processed_data))