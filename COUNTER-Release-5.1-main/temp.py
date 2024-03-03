import json
from faker import Faker
import random
from random import randint

fake = Faker("en_US")

ans = []
for _ in range(170):
    version = random.choice(["5.0", "5.1"])
    base_url = f"{fake.url()}{'r51/' if version == '5.1' else ''}reports"

    my_dict = {
        "name": fake.name(),
        "version": version,
        "base_url": base_url,
        "starting_year": fake.date()[0:4],
        "customer_id": fake.aba(),
        "requestor_id": fake.aba(),
        "api_key": fake.uuid4(),
        "platform": fake.uuid4()[0:7],
        "requires_two_attempts": str(fake.boolean()).lower(),
        "does_ip_checking": str(fake.boolean()).lower(),
        "needs_throttling": str(fake.boolean()).lower(),
        "notes": fake.text()[0:20],
        "provider": fake.text()[0:10],
    }
    ans.append(my_dict)

print(ans)
