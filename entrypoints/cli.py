import argparse
import datetime
from ssn_generation.core.usecases.pesel_generator import generate_unique_ssn
from ssn_generation.dataproviders.faker_ssn_provider import generate_ssn_with_faker
from ssn_generation.core.entities.pesel import Pesel

def _print_pesels(pesel_list: list[str], source: str):
    print(f"Generated {len(pesel_list)} PESELs with {source}:")
    for pesel in pesel_list:
        print(pesel)

def main():
    parser = argparse.ArgumentParser(description="Polish SSN (PESEL) generator and validator.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Generator subparser
    parser_gen = subparsers.add_parser('generate', help='Generate PESEL numbers.')
    parser_gen.add_argument('num', type=int, help='Number of PESELs to generate.')
    parser_gen.add_argument('--method', type=str, default='unique', choices=['unique', 'faker'],
                              help='Generation method: "unique" for custom implementation, "faker" for faker-based generation.')
    parser_gen.add_argument('--sex', type=str, help='Sex (M/F). Required for "unique" method.')
    parser_gen.add_argument('--start-date', type=str, help='Start date for birth date (YYYY-MM-DD). Required for "unique" method.')
    parser_gen.add_argument('--end-date', type=str, help='End date for birth date (YYYY-MM-DD). Required for "unique" method.')

    # Validator subparser
    parser_val = subparsers.add_parser('validate', help='Validate a PESEL number.')
    parser_val.add_argument('pesel', type=str, help='PESEL to validate.')
    parser_val.add_argument('--sex', type=str, help='Sex to validate against (M/F).')
    parser_val.add_argument('--birth-date', type=str, help='Birth date to validate against (YYYY-MM-DD).')


    args = parser.parse_args()

    if args.command == 'generate':
        try:
            if args.method == 'unique':
                if not all([args.sex, args.start_date, args.end_date]):
                    parser.error("--sex, --start-date, and --end-date are required for the 'unique' method.")
                
                start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d').date()
                
                pesels = generate_unique_ssn(args.num, args.sex, start_date, end_date)
                _print_pesels(pesels, "unique method")
            elif args.method == 'faker':
                pesels = generate_ssn_with_faker(args.num)
                _print_pesels(pesels, "Faker")
        except ValueError as e:
            parser.error(str(e))

    elif args.command == 'validate':
        birth_date = datetime.datetime.strptime(args.birth_date, '%Y-%m-%d').date() if args.birth_date else None
        p = Pesel(args.pesel)
        is_valid = p.is_valid(sex=args.sex, birth_date=birth_date)
        if is_valid:
            print(f"PESEL {args.pesel} is valid.")
        else:
            print(f"PESEL {args.pesel} is invalid.")

if __name__ == '__main__':
    main() 