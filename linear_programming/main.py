from argparse import ArgumentParser
from linear_programming.utils.linear_program_generator import generate_to_file


def main():
    parser = ArgumentParser(prog='linear_programming',
                            description='Honours Project for Irving Ou')

    subparsers = parser.add_subparsers(
        help='generate linear program ', dest='command')

    gen_parser = subparsers.add_parser('generate')

    gen_parser.add_argument('-n', '--num_constrains', type=int)
    gen_parser.add_argument('-f', '--file_name', type=str)

    solve_parser = subparsers.add_parser('solve')
    solve_parser.add_argument('-f', '--file_name', type=str)

    args = parser.parse_args()

    if args.command == 'generate':
        file = generate_to_file(num_of_constraints=args.num_constrains)
        print(f"Generated file: {file}")

    elif args.command == 'solve':
        raise NotImplementedError()
