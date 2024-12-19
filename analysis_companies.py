import json
import re
from collections import defaultdict
from tqdm import tqdm


class Company(dict):
    def __init__(self, input_dict):
        super().__init__(input_dict)

    def __key(self):
        """
        Create a tuple of attributes used for comparison and hashing.
        """
        # Use specific keys to determine equality and hashing
        return (self.get("name"), self.get("website"), self.get("year_of_founding"))

    def __hash__(self):
        """
        Hash the object based on the selected attributes.
        """
        return hash(self.__key())

    def __eq__(self, other):
        """
        Compare two Company objects for equality based on selected attributes.
        """
        if not isinstance(other, Company):
            return False
        return self.__key() == other.__key()


def process_company_entry(company):
    """Process a single company entry with advanced NER extraction."""
    sector = str(company.get("sector"))

    sector = [s.strip() for s in re.split(r'[;,/]', sector) if s.strip()]

    company["sector"] = sector

    return company


# missing, duplicates, corrections

# Total: 878 After filteration: 675
# Number of missing company names: 203
# Number of duplicates found: 1


if __name__ == "__main__":
    input_file = "company_data_.json"
    input_file_cleaned = "cleaned_company_data.json"

    # open file with companies
    with open(input_file, "r", encoding="utf-8") as fin1:
        raw_data = json.load(fin1)


    simple_set = set()
    company_stats = defaultdict(int)

    # process companies and count empty ones
    empty_name = 0
    processed_data = []
    for id, company in enumerate(tqdm(raw_data)):
        company = Company(company)
        company['id'] = id

        simple_set.add(company)

        if company['name'] is None:
            empty_name += 1

        # process each company
        if company['name'] is not None:
            processed_entry = process_company_entry(company)
            processed_data.append(processed_entry)

            company_stats[(company.get("name"), company.get("website"), company.get("year_of_founding"))] += 1

    
    # print the main numbers
    print("Total:", len(processed_data) + empty_name, "After filteration:", len(processed_data))
    print("Number of missing company names:", empty_name)
    print("Number of duplicates found:", len(simple_set) - len(processed_data))

    # processed companies that could be used later
    processed_data = list(set(processed_data))