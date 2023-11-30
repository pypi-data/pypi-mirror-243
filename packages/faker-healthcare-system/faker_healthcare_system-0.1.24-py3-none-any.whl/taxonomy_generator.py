import csv
import importlib.resources
import random
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass(frozen=True)
class TaxonomyEntity:
    code: str
    classification: str
    specialization: str
    section: str
    grouping: str
    display_name: str


class TaxonomyGenerator:
    TAXONOMY_CSV_DIR = importlib.resources.files("assets") / "nucc_taxonomy_231.csv"

    def __init__(self):
        self.taxonomy_data, self.taxonomy_individual_data = self.load_taxonomy_data()

    def load_taxonomy_data(self):
        taxonomy_data = {}
        taxonomy_only_individual_data = {}
        try:
            with open(self.TAXONOMY_CSV_DIR, newline="") as csv_file:
                reader = csv.reader(csv_file, delimiter=",")
                next(reader)
                for row in reader:
                    code = row[0]
                    taxonomy = TaxonomyEntity(
                        code=row[0],
                        grouping=row[1],
                        classification=row[2],
                        specialization=row[3],
                        display_name=row[6],
                        section=row[7],
                    )
                    if taxonomy.section.lower() == "individual":
                        taxonomy_only_individual_data[code] = taxonomy
                    taxonomy_data[code] = taxonomy
        except FileNotFoundError:
            print(f"File '{self.TAXONOMY_CSV_DIR}' could not be found.")
        return taxonomy_data, taxonomy_only_individual_data

    def get_taxonomy_codes(self) -> List[str]:
        return list(self.taxonomy_data.keys())

    def get_individuals_taxonomy_codes(self) -> List[str]:
        return list(self.taxonomy_individual_data.keys())

    def find_by_code(self, code: str) -> Optional[TaxonomyEntity]:
        return self.taxonomy_data.get(code, None)

    def get_random_taxonomy(self) -> TaxonomyEntity:
        return self.find_by_code(random.choice(self.get_taxonomy_codes()))

    def get_random_individual_taxonomy(self) -> TaxonomyEntity:
        return self.find_by_code(random.choice(self.get_individuals_taxonomy_codes()))

    def get_uniques_taxonomies_individuals(self, quantity: int) -> List[dict]:
        unique_taxonomies = set()
        while len(unique_taxonomies) < quantity:
            unique_taxonomies.add(self.get_random_individual_taxonomy())
        return [asdict(taxonomy) for taxonomy in list(unique_taxonomies)]
