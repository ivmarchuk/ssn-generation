from dataclasses import dataclass
from datetime import date
from ssn_generation.core.entities.pesel_rules import get_check_digit, valid_month_value

@dataclass
class Pesel:
    value: str

    def __post_init__(self):
        self.value = str(self.value)

    def _has_valid_format(self) -> bool:
        return self.value.isdigit() and len(self.value) == 11

    def _has_valid_birth_date(self, birth_date: date | None) -> bool:
        if not birth_date:
            return True
        
        year = str(birth_date)[2:4]
        month = valid_month_value(birth_date)
        day = birth_date.strftime('%d')
        
        return self.value[0:2] == year and self.value[2:4] == month and self.value[4:6] == day

    def _has_valid_sex(self, sex: str | None) -> bool:
        if not sex:
            return True
        
        sex_digit = int(self.value[-2])
        sex_upper = sex.upper()

        if sex_upper == 'M':
            return sex_digit % 2 == 1
        if sex_upper == 'F':
            return sex_digit % 2 == 0
        
        return False

    def _has_valid_checksum(self) -> bool:
        return int(self.value[-1]) == get_check_digit(self.value)

    def is_valid(self, sex: str | None = None, birth_date: date | None = None) -> bool:
        return all([
            self._has_valid_format(),
            self._has_valid_birth_date(birth_date),
            self._has_valid_sex(sex),
            self._has_valid_checksum()
        ]) 