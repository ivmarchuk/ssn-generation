import datetime
import random
from faker import Faker
import pandas as pd

from ssn_generation.core.entities.pesel_rules import get_check_digit, valid_month_value
from ssn_generation.core.utils.decorators import measure_time


def _calculate_max_pesels(start_date: datetime.date, end_date: datetime.date) -> int:
    """Calculates the max possible unique PESELs for a given date range."""
    if start_date > end_date:
        return 0
    
    number_of_days = (end_date - start_date).days + 1
    # For each day, there are 1000 possible "xxx" combinations (000-999)
    # and 5 possible sex digits for a given sex (e.g., 1,3,5,7,9 for M)
    return number_of_days * 1000 * 5


@measure_time
def generate_unique_ssn(num: int, sex: str, start_date: datetime.date, end_date: datetime.date) -> list[str]:
    fake = Faker()
    pesels = set()
    
    max_possible = _calculate_max_pesels(start_date, end_date)
    if num > max_possible:
        raise ValueError(f"Cannot generate {num} unique PESELs. The maximum possible for the given date range and sex is {max_possible}.")

    while len(pesels) != num:

        # Get year value
        birth_date = fake.date_between(start_date=start_date, end_date=end_date)
        year = str(birth_date)[2:4]

        # Get month value
        month = valid_month_value(birth_date)

        # Get day value
        day = birth_date.strftime('%d')

        # XXX - random number
        xxx = f"{random.randint(0, 999):03d}"

        # G – random digit indicates person's gender (odd number is for male, even – for female)
        if sex.upper() == 'M':
            s = str(random.randrange(1, 10, step=2))
        elif sex.upper() == 'F':
            s = str(random.randrange(0, 10, step=2))
        else:
            raise ValueError("Wrong sex char provided. Use 'M' or 'F'.")

        # get 10 digits of pesel to generate check digit
        pesel_10_digits = year + month + day + xxx + s

        # Get check digit
        k = get_check_digit(pesel_10_digits)
        pesel = pesel_10_digits + str(k)

        # Validate if pesel is unique
        pesels.add(pesel)

    return list(pesels) 