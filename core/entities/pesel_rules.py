import datetime

_CENTURY_OFFSETS = [
    (1800, 1899, 80),
    (2000, 2099, 20),
    (2100, 2199, 40),
    (2200, 2299, 60),
]

def valid_month_value(birth_date: datetime.date) -> str:
  '''https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Poland-TIN.pdf
    Based on the above document, the 3rd and 4th digits in the pesel number are generated based on the month from the person's date of birth. 
    Depending on the century in which the person was born, a number is added to the value of the month. 
    This function verifies the entered month value and outputs the correct month digits for pesel generation. '''

  year = birth_date.year
  month = birth_date.month

  for start_year, end_year, offset in _CENTURY_OFFSETS:
      if start_year <= year <= end_year:
          return str(month + offset)
          
  # Default case for 1900-1999, which has no offset
  return f"{month:02d}"


def get_check_digit(pesel: str) -> int:
  '''The check digit is generated last, based on the remaining digits in the pesel number.
      This function gives the logic for generating such a number.
      Formula: 10 - (last_digit_of_sum(c1*1 + c2*3 + c3*7 + c4*9 + c5*1 + c6*3 + c7*7 + c8*9 + c9 *1 + c10*3))
      For more https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Poland-TIN.pdf''' 

  weights = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
  formula_sum = sum(int(digit) * weight for digit, weight in zip(pesel, weights))
        
  # get the last digit of formula sum (we are sure, that the number will be > 0)
  formula_last_digit = formula_sum % 10
  
  check_digit = 10 - formula_last_digit
  
  return check_digit if check_digit != 10 else 0 