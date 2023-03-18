from argparse import ArgumentParser
import argparse
import re
from linear_programming.utils.linear_program_generator import generate_to_file_bounded, generate_to_file_infeasible
import linear_programming.utils.compare_time as compare_time


def main():
    parser = ArgumentParser(prog='linear_programming',
                            description='Honours Project for Irving Ou')

    subparsers = parser.add_subparsers(
        help='generate linear program ', dest='command')

    gen_parser = subparsers.add_parser('generate')

    gen_parser.add_argument('-n', '--num_constrains', type=int)
    gen_parser.add_argument('-t', '--type', type=str,choices=['bounded','infeasible'])
    gen_parser.add_argument('-f', '--file_name', type=str)

    solve_parser = subparsers.add_parser('solve')
    solve_parser.add_argument('-f', '--file_name', type=str)

  
    
    solve_parser = subparsers.add_parser('test')
    def range_type(arg_value, pat=re.compile(r"^\d+,\d+,\d+$")):
        if not pat.match(arg_value):
            raise argparse.ArgumentTypeError("invalid value")
        return arg_value
    solve_parser.add_argument('-r', '--range', type=range_type)

    args = parser.parse_args()

    if args.command == 'generate':
        file = generate_to_file_bounded(num_of_constraints=args.num_constrains) if args.type == 'bounded' else generate_to_file_infeasible(num_of_constraints=args.num_constrains)
        print(f"Generated file: {file}")

    elif args.command == 'solve':
        raise NotImplementedError()
    
    elif args.command == 'test':
        compare_time.test_data_feasible(range(100,100000,100))
        
