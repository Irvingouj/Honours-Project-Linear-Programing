import os
from typing import List
from linear_programming.classes.constraints import Constraints
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.utils.linear_program_generator import LINEAR_PROGRAMS_DIR


def save_to_file(file_type:str,obj:ObjectiveFunction,constraints:List[Constraints])->str:
    assert file_type in ["bounded", "unbounded", "infeasible"]
    file_prefix = f"{file_type}_problem"
    
    files = [f for f in os.listdir(
        LINEAR_PROGRAMS_DIR) if f.startswith(file_prefix)]
    
    file_name = f"{file_prefix}{len(files)+1}"
    file_path = os.path.join(LINEAR_PROGRAMS_DIR, file_name)
    file = open(file_path, 'w', encoding='utf-8')
    file.write(f"# type = {file_type} problem generated randomly,n = {len(constraints)}\n")
    file.write(str(obj))
    for con in constraints:
        file.write("\n")
        file.write(str(con))
    file.close()
    return file_path   