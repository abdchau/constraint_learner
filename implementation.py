"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
from itertools import product

def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:
    num_of_nts = constraint_pattern.count("{}")
    cartesian = product(nonterminals, repeat=num_of_nts)
    
    return {constraint_pattern.format(*nts) for nts in cartesian}

def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:
    pass

def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:
    pass

def check(abstract_constraints: set[str], derivation_tree) -> bool:
    pass

def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:
    pass