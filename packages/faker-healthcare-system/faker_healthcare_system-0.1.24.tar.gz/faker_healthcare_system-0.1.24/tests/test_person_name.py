import pytest
from faker import Faker

from faker_healthcare_system import PersonNameProvider


@pytest.fixture
def fake():
    fake_instance = Faker()
    fake_instance.add_provider(PersonNameProvider)
    return fake_instance


def test_person_name(fake):
    generated_name = fake.person_name()
    assert isinstance(generated_name, str)


def test_person_object(fake):
    person_data = fake.person_object()

    assert "first_name" in person_data
    assert isinstance(person_data["first_name"], str)

    assert "last_name" in person_data
    assert isinstance(person_data["last_name"], str)

    assert "name_prefix" in person_data
    assert isinstance(person_data["name_prefix"], str)

    assert "name_suffix" in person_data
    assert isinstance(person_data["name_suffix"], str)

    assert "type_name" in person_data
    assert person_data["type_name"] == "Personal Name"


def test_person_object_by_gender(fake):
    male_data = fake.person_object_by_gender("M")
    female_data = fake.person_object_by_gender("F")

    assert "first_name" in male_data
    assert isinstance(male_data["first_name"], str)

    assert "last_name" in male_data
    assert isinstance(male_data["last_name"], str)

    assert "name_prefix" in male_data
    assert isinstance(male_data["name_prefix"], str)

    assert "name_suffix" in male_data
    assert isinstance(male_data["name_suffix"], str)

    assert "type_name" in male_data
    assert male_data["type_name"] == "Personal Name"

    assert "first_name" in female_data
    assert isinstance(female_data["first_name"], str)

    assert "last_name" in female_data
    assert isinstance(female_data["last_name"], str)

    assert "name_prefix" in female_data
    assert isinstance(female_data["name_prefix"], str)

    assert "name_suffix" in female_data
    assert isinstance(female_data["name_suffix"], str)

    assert "type_name" in female_data
    assert female_data["type_name"] == "Personal Name"


def test_person_object_married(fake):
    initial_data = {
        "first_name": "John",
        "last_name": "Doe",
        "name_prefix": "Mr.",
        "name_suffix": "Jr.",
        "type_name": "Single",
    }

    married_data = fake.person_object_married(initial_data)

    assert "first_name" in married_data
    assert married_data["first_name"] == initial_data["first_name"]

    assert "last_name" in married_data
    assert isinstance(married_data["last_name"], str)

    assert "name_prefix" in married_data
    assert married_data["name_prefix"] == initial_data["name_prefix"]

    assert "name_suffix" in married_data
    assert married_data["name_suffix"] == initial_data["name_suffix"]

    assert "type_name" in married_data
    assert married_data["type_name"] == "Married"
