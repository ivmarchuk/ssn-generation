from faker import Faker
from faker.providers.ssn.pl_PL import Provider as SsnProvider
import pandas as pd

from ssn_generation.core.utils.decorators import measure_time

# Instantiate Faker once at the module level for efficiency
_fake = Faker()
_fake.add_provider(SsnProvider)

@measure_time
def generate_ssn_with_faker(num: int) -> list[str]:
    '''Generates a random valid pesel number using faker library.
       As input takes the amount of PESEL values to be generated '''
    # According to faker docs we can guarantee that any generated values are unique for this specific instance.
    return [_fake.unique.ssn() for _ in range(num)] 