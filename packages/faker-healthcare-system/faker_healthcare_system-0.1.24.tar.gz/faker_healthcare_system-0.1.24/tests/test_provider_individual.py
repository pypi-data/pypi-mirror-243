import pytest
from datetime import date

from faker import Faker

from faker_healthcare_system import IndividualProvider, PersonNameProvider


@pytest.fixture
def fake():
    fake_instance = Faker()
    fake_instance.add_provider(IndividualProvider)
    fake_instance.add_provider(PersonNameProvider)
    return fake_instance


def test_npi_is_nine_digits(fake):
    npi = fake.npi()
    assert isinstance(npi, int)
    assert len(str(npi)) == 9


def test_tin_is_nine_digits(fake):
    tin = fake.tin()
    assert isinstance(tin, int)
    assert len(str(tin)) == 9


def test_gender_is_valid(fake):
    gender = fake.gender()
    assert gender in ["M", "F"]


def test_enumeration_date_is_date_object(fake):
    enumeration_date = fake.enumeration_date()
    assert isinstance(enumeration_date, date)


def test_taxonomy_returns_dict(fake):
    taxonomy = fake.taxonomy()
    assert isinstance(taxonomy, dict)
    assert set(taxonomy.keys()) == {
        "code",
        "classification",
        "specialization",
        "section",
        "grouping",
        "display_name",
    }


def test_individual_taxonomies_returns_list(fake):
    quantity = 3
    taxonomies = fake.individual_taxonomies(quantity)
    assert isinstance(taxonomies, list)
    assert len(taxonomies) == quantity


def test_person_name_by_gender_returns_dict(fake):
    gender = "F"
    person_name = fake.person_name_by_gender(gender)
    assert isinstance(person_name, dict)
    assert set(person_name.keys()) == {
        "first_name",
        "last_name",
        "name_prefix",
        "name_suffix",
        "type_name",
    }
    assert person_name["type_name"] == "Personal Name"


def test_individual_object_contains_required_fields(fake):
    individual = fake.individual_object()
    assert "npi" in individual
    assert "tin" in individual
    assert "last_updated_epoch" in individual
    assert "created_epoch" in individual
    # Agrega más campos según sea necesario


def test_individual_object_addresses_have_purpose(fake):
    individual = fake.individual_object()
    assert (
        "mailing_address" in individual
        and individual["mailing_address"]["purpose"] == "Mailing"
    )
    assert (
        "location_address" in individual
        and individual["location_address"]["purpose"] == "LOCATION"
    )
    assert (
        "main_office_address" in individual
        and individual["main_office_address"]["purpose"] == "Main Office"
    )


def test_practitioner_languages_plus_english_contains_english(fake):
    quantity = 5
    languages = fake.practitioner_languages_plus_english(quantity)
    english_exists = any(lang["code"] == "en" for lang in languages)
    assert english_exists


def test_license_contains_required_fields(fake):
    license_info = fake.license()
    assert "license" in license_info
    assert "state" in license_info
    assert "is_primary" in license_info
    assert "start_date" in license_info
    assert "end_date" in license_info


def test_dea_contains_required_fields(fake):
    dea_info = fake.dea()
    assert "number" in dea_info
    assert "allow_prescribe" in dea_info
    assert "start_date" in dea_info
    assert "expiration_date" in dea_info
    assert "supervising_number" in dea_info
    assert "supervising_license" in dea_info


def test_malpractice_contains_required_fields(fake):
    malpractice_info = fake.malpractice()
    assert "insurance" in malpractice_info
    assert "insurance_policy_number" in malpractice_info
    assert "covered_amount" in malpractice_info
