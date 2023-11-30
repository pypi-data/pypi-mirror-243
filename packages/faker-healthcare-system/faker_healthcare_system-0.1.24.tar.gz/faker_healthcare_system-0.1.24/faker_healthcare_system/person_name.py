from faker.providers import BaseProvider


class PersonNameProvider(BaseProvider):
    def person_name(self):
        return self.generator.last_name_male()

    def person_object(self) -> dict:
        return {
            "first_name": self.generator.first_name(),
            "last_name": self.generator.last_name(),
            "name_prefix": self.generator.prefix(),
            "name_suffix": self.generator.suffix(),
            "type_name": "Personal Name",
        }

    def person_object_by_gender(self, gender: str) -> dict:
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

    def person_object_married(self, person_object: dict) -> dict:
        new_last_name = self.generator.last_name_male()

        new_person_object = {
            "first_name": person_object["first_name"],
            "last_name": new_last_name,
            "name_prefix": person_object["name_prefix"],
            "name_suffix": person_object["name_suffix"],
            "type_name": "Married",
        }
        return new_person_object
