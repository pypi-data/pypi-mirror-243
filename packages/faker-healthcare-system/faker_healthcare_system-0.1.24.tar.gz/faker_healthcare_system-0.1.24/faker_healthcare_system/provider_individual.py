import random
from collections import OrderedDict
from datetime import date, timedelta
from typing import List

from faker import Faker
from faker.providers import BaseProvider

from taxonomy_generator import TaxonomyGenerator
from constants import (
    ADDRESS_TYPE,
    MEDICAL_UNIVERSITIES_USA,
    ISO_639_LANGUAGES,
    ETHNICITY,
    MALPRACTICE_INSURANCE,
    ENDPOINT_TYPE,
    ENDPOINT_USE,
    ENDPOINT_CONTENT_OTHER_DESCRIPTION,
    CREDENTIAL,
    US_STATES, OFFICIAL_TITLE_POSITION,
)


class IndividualProvider(BaseProvider):
    __taxonomy = TaxonomyGenerator()

    def npi(self) -> int:
        return self.generator.random_number(digits=9, fix_len=True)

    def tin(self) -> int:
        return self.generator.random_int(min=100000000, max=999999999)

    def gender(self) -> str:
        return random.choice(["M", "F"])

    def enumeration_date(self) -> date:
        return self.generator.date_between(start_date="-5y", end_date="today")

    def taxonomy(self):
        return self.__taxonomy.get_random_taxonomy().__dict__

    def individual_taxonomies(self, quantity: int) -> List[dict]:
        taxonomies_list = self.__taxonomy.get_uniques_taxonomies_individuals(quantity)
        return [tax for tax in taxonomies_list]

    def individual_unique_taxonomies(self, quantity: int):
        return self.__taxonomy.get_uniques_taxonomies_individuals(quantity)

    def person_name_by_gender(self, gender: str) -> dict:
        return {
            "first_name": self.generator.first_name_female()
            if gender == "F"
            else self.generator.first_name_male(),
            "last_name": self.generator.last_name_female()
            if gender == "F"
            else self.generator.last_name_male(),
            "name_prefix": self.generator.prefix_female()
            if gender == "F"
            else self.generator.prefix_male(),
            "name_suffix": self.generator.suffix_female()
            if gender == "F"
            else self.generator.suffix_male(),
            "type_name": "Personal Name",
        }

    def fullname(self):
        return f"{self.generator.first_name()} {self.generator.last_name()}"

    def person_married_name(self, person_object: dict) -> dict:
        new_last_name = self.generator.last_name_male()

        new_person_object = {
            "first_name": person_object["first_name"],
            "last_name": new_last_name,
            "name_prefix": person_object["name_prefix"],
            "name_suffix": person_object["name_suffix"],
            "type_name": "Married",
        }
        return new_person_object

    def address_with_purpose(self, purpose: str = "Mailing") -> dict:
        return {
            "country_code": self.generator.current_country_code(),
            "country_name": self.generator.current_country(),
            "purpose": purpose,
            "address_type": random.choice(ADDRESS_TYPE)
            if purpose != "Main Office"
            else "Physical",
            "address_1": self.generator.address(),
            "address_2": self.generator.address(),
            "city": self.generator.city(),
            "state": random.choice(US_STATES),
            "postal_code": self.generator.postcode(),
            "telephone_number": self.generator.phone_number(),
            "fax_number": self.generator.phone_number(),
        }

    def dea(self) -> dict:
        start_date: date = self.generator.date_this_decade()
        return {
            "number": f"{random.choice(['A', 'C', 'M'])}{self.generator.random_int(min=1000000, max=9999999)}",
            "allow_prescribe": self.generator.boolean(),
            "start_date": start_date,
            "expiration_date": start_date
                               + timedelta(365 * self.generator.random_int(min=1, max=4)),
            "supervising_number": f"{random.choice(['X', 'Y'])}{self.generator.random_int(min=1000000, max=9999999)}",
            "supervising_license": self.generator.random_int(min=1000000, max=9999999),
        }

    def professional_degree_school(self) -> str:
        return random.choice(MEDICAL_UNIVERSITIES_USA)

    def practitioner_language(self) -> dict:
        lang: tuple[str, str] = random.choice(ISO_639_LANGUAGES)
        return {
            "code": lang[1].upper(),
            "description": lang[0],
            "language_type": "Practitioner",
        }

    def practitioner_languages_plus_english(self, quantity: int) -> List[dict]:
        list_languages: List[dict] = []
        english = {
            "code": "en",
            "description": "English",
            "language_type": "Practitioner",
        }
        english_exist: bool = False
        for _ in range(quantity):
            language: dict = self.practitioner_language()
            list_languages.append(language)
            if language["code"] == "en":
                english_exist = True
        return list_languages if english_exist else list_languages + [english]

    def practitioner_ethnicity_code(self) -> dict:
        random_key, random_value = random.choice(list(ETHNICITY.items()))
        return {"code": random_key, "description": random_value}

    def gender_restriction(self) -> str:
        return self.generator.random_element(
            elements=OrderedDict(
                [
                    ("F", 0.1),  # Generates "variable_1" 50% of the time
                    ("M", 0.1),  # Generates "variable_2" 20% of the time
                    ("NR", 0.8),  # Generates "variable_3" 20% of the time
                ]
            )
        )

    def malpractice(self) -> dict:
        return {
            "insurance": random.choice(MALPRACTICE_INSURANCE),
            "insurance_policy_number": self.generator.random_number(fix_len=True),
            "covered_amount": f" {self.generator.random_int(min=0, max=9)}-{self.generator.random_int(min=0, max=9)}",
        }

    def license(self) -> dict:
        start_date: date = self.generator.date_this_decade()
        return {
            "license": f"{self.generator.random_uppercase_letter()}{self.generator.random_number(digits=9)}",
            "state": random.choice(US_STATES),
            "is_primary": self.generator.boolean(),
            "start_date": start_date,
            "end_date": start_date
                        + timedelta(365 * self.generator.random_int(min=1, max=4)),
        }

    def identifier(self) -> dict:
        return {
            "code": self.generator.random_int(),
            "desc": random.choice(["Other (non-Medicare)", "Medicare"]),
            "issuer": self.generator.bothify(text="????"),
            "identifier": self.generator.bothify(text="#####"),
            "state": random.choice(US_STATES),
        }

    def board(self) -> dict:
        start_date = self.generator.date_this_decade()
        return {
            "status": random.choice([1, 2, 3, 4, 5]),
            "start_date": start_date,
            "expiration_date": start_date
                               + timedelta(365 * self.generator.random_int(min=1, max=4)),
        }

    def taxonomy_qualification(self, taxonomy: dict | None = None) -> dict:
        start_date = self.generator.date_this_decade()
        qualification = {
            "board": self.board(),
            "intership_start_date": start_date,
            "intership_expiration_date": start_date
                                         + timedelta(365 * self.generator.random_int(min=1, max=4)),
            "residency_start_date": start_date,
            "residency_expiration_date": start_date
                                         + timedelta(365 * self.generator.random_int(min=1, max=4)),
            "fellowship_start_date": start_date,
            "fellowship_expiration_date": start_date
                                          + timedelta(365 * self.generator.random_int(min=1, max=4)),
            "taxonomy": self.taxonomy() if taxonomy is None else taxonomy,
            "facility_type": 10,
        }
        return qualification

    def endpoint(self) -> dict:
        content = random.choice(["OTHER", "CSV"])
        content_other_description = random.choice(ENDPOINT_CONTENT_OTHER_DESCRIPTION)
        endpoint_code: str = random.choice(list(ENDPOINT_TYPE.keys()))
        use_code: str = random.choice(list(ENDPOINT_USE.keys()))
        return {
            "endpointType": endpoint_code,
            "endpointTypeDescription": ENDPOINT_TYPE[endpoint_code],
            "endpoint": self.generator.ascii_company_email()
            if endpoint_code == "DIRECT"
            else self.generator.uri(),
            "endpointDescription": "",
            "affiliation": random.choice(["Y", "N"]),
            "use": use_code,
            "useDescription": ENDPOINT_USE[use_code],
            "contentType": content,
            "contentTypeDescription": content_other_description,
            "contentOtherDescription": content_other_description,
            "country_code": "US",
            "country_name": "United States",
            "address_1": self.generator.address(),
            "city": self.generator.city(),
            "state": random.choice(US_STATES),
            "postal_code": self.generator.postcode(),
        }

    def working_hours(self) -> str:
        start_hour = self.generator.random_int(min=7, max=10)
        end_hour = self.generator.random_int(min=start_hour + 2, max=20)
        return f"{start_hour}:00-{end_hour}:00"

    def weekly_working_hours(self) -> dict:
        return {
            "Monday": self.working_hours(),
            "Tuesday": self.working_hours(),
            "Wednesday": self.working_hours(),
            "Thursday": self.working_hours(),
            "Friday": self.working_hours(),
            "Saturday": random.choice(["CLOSED", self.working_hours()]),
            "Sunday": "CLOSED",
        }

    def organization_type(self):
        return random.choice(['Official', 'Doing Business As'])

    def __taxonomy_qualification_by_taxonomies(
            self, taxomonies: List[dict]
    ) -> List[dict]:
        qualifications: List[dict] = []
        for taxonomy in taxomonies:
            qualifications.append(self.taxonomy_qualification(taxonomy))
        return qualifications

    def individual_object(self) -> dict:
        gender = self.gender()
        person_name: dict = self.generator.person_name_by_gender(gender)
        last_updated_epoch: date = self.generator.date_this_decade()
        created_epoch = last_updated_epoch - timedelta(
            365 * self.generator.random_int(min=1, max=4)
        )
        languages = self.practitioner_languages_plus_english(6)
        credential = random.choice(CREDENTIAL)
        sole_proprietor = random.choice(["YES", "NO"])
        ethnicity_code = self.practitioner_ethnicity_code()["code"]
        identifier = self.identifier()
        taxonomies: List[dict] = self.individual_unique_taxonomies(4)
        taxonomy_qualification = self.__taxonomy_qualification_by_taxonomies(taxonomies)
        return {
            "npi": self.npi(),
            "tin": self.tin(),
            "last_updated_epoch": last_updated_epoch,
            "created_epoch": created_epoch,
            "enumeration_date": self.enumeration_date(),
            "status": "Active",
            "email": self.generator.email(),
            "enumeration_type": "NPI-1",
            "mailing_address": self.address_with_purpose(),
            "location_address": self.address_with_purpose(purpose="LOCATION"),
            "main_office_address": self.address_with_purpose(purpose="Main Office"),
            "taxonomies": taxonomies,
            "licenses": [self.license() for _ in range(9)],
            "identifiers": identifier,
            "taxonomy_qualification": taxonomy_qualification,
            "taxonomy_endpoints": self.endpoint(),
            "office_hours": self.weekly_working_hours(),
            "telehealth_hours": self.weekly_working_hours(),
            "credential": credential,
            "sole_proprietor": sole_proprietor,
            "gender": gender,
            "personal_name": person_name,
            "other_names": ""
            if gender == "M"
            else self.person_married_name(person_name),
            "dea": self.dea(),
            "ethnicity_code": ethnicity_code,
            "date_of_birth": self.generator.date_of_birth(),
            "languages": languages,
            "gender_restriction": self.gender_restriction(),
            "malpractice": self.malpractice(),
            "professional_degree_school": self.professional_degree_school(),
        }

    def organization_object(self, max_npi: int = 1) -> dict:
        npi = self.npi() if max_npi == 1 else [self.npi() for _ in range(max_npi)]
        gender = self.gender()
        person_name: dict = self.generator.person_name_by_gender(gender)
        person_authorized: str = self.generator.fullname()
        last_updated_epoch: date = self.generator.date_this_decade()
        created_epoch = last_updated_epoch - timedelta(
            365 * self.generator.random_int(min=1, max=4)
        )
        languages = self.practitioner_languages_plus_english(6)
        credential = random.choice(CREDENTIAL)
        sole_proprietor = random.choice(["YES", "NO"])
        identifier = self.identifier()
        taxonomies: List[dict] = self.individual_unique_taxonomies(4)
        return {
            "npi": npi,
            "tin": self.tin(),
            "last_updated_epoch": last_updated_epoch,
            "created_epoch": created_epoch,
            "enumeration_date": self.enumeration_date(),
            "status": "Active",
            "email": self.generator.email(),
            "enumeration_type": "NPI-2",
            "mailing_address": self.address_with_purpose(),
            "location_address": self.address_with_purpose(purpose="LOCATION"),
            "main_office_address": self.address_with_purpose(purpose="Main Office"),
            "taxonomies": taxonomies,
            "licenses": [self.license() for _ in range(9)],
            "identifiers": identifier,
            # "taxonomy_qualification": '',
            # "taxonomy_endpoints": '',
            # "office_hours": '',
            # "telehealth_hours": '',
            "credential": credential,
            "sole_proprietor": sole_proprietor,
            "gender": gender,
            "personal_name": person_name,
            "other_names": "",
            "dea": self.dea(),
            "ethnicity_code": '',
            "date_of_birth": '',
            "languages": languages,
            "gender_restriction": '',
            "malpractice": self.malpractice(),
            "professional_degree_school": '',
            "organization_name": self.generator.company(),
            "organization_subpart": random.choice(['YES', 'NO']),
            "organization_type": self.organization_type(),
            "person_authorized": person_authorized,
            "person_authorized_title_or_position": random.choice(OFFICIAL_TITLE_POSITION),
            "other_organization_name_1": self.generator.company(),
            "other_organization_subpart_1": random.choice(['YES', 'NO']),
            "other_organization_type_1": self.organization_type(),
            "other_organization_name_2": self.generator.company(),
            "other_organization_subpart_2": random.choice(['YES', 'NO']),
            "other_organization_type_2": self.organization_type(),
            "pcmh_status": self.generator.random_int(min=1, max=4),
        }


fake = Faker()
fake.add_provider(IndividualProvider)
Faker.seed(153)

print(fake.weekly_working_hours())

fake_person_names = [fake.organization_object(max_npi=3) for _ in range(1)]
for i in fake_person_names:
    print(i)
    print(i['npi'])
