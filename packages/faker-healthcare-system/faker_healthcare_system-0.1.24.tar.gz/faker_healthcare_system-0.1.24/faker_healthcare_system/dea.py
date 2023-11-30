import random
from datetime import date, timedelta

from faker import Faker
from faker.providers import BaseProvider


class DeaProvider(BaseProvider):
    def dea_object(self) -> dict:
        start_date: date = self.generator.date_this_decade()
        return {
            "number": f"{random.choice(['A', 'C', 'M'])}{self.generator.random_int(min=1000000, max=9999999)}",
            "allow_prescribe": self.generator.boolean(),
            "start_date": self.generator.date_this_decade(),
            "expiration_date": start_date + timedelta(days=365 * 5),
            "supervising_number": f"{random.choice(['X', 'Y'])}{self.generator.random_int(min=1000000, max=9999999)}",
            "supervising_license": self.generator.random_int(min=1000000, max=9999999),
        }


fake = Faker()
fake.add_provider(DeaProvider)
Faker.seed(0)

fake_data = [fake.dea_object() for _ in range(10)]
for i in fake_data:
    print(i)
