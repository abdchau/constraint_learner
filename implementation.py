"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
from itertools import product
from fuzzingbook.Grammars import nonterminals

from helpers import tree_to_string

def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:
    num_of_nts = constraint_pattern.count("{}")
    cartesian = product(nonterminals, repeat=num_of_nts)
    
    return {constraint_pattern.format(*nts) for nts in cartesian}

#---------------------------------------------------------------------------------------------------

def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:
    nts = nonterminals(abstract_constraint)

    nts_to_string = {nt: [tree_to_string(subtree) for subtree in subtrees] 
                            for nt, subtrees in nts_to_subtrees.items()}

    replacers = [nts_to_string[nt] for nt in nts]
    cartesian = list(product(*replacers, repeat=1))
    
    result = set()
    for replacements in cartesian:
        concrete_constraint = abstract_constraint

        for i, nt in enumerate(nts):
            concrete_constraint = concrete_constraint.replace(nt, replacements[i], 1)

        result.add(concrete_constraint)

    return result

#---------------------------------------------------------------------------------------------------

def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:
    pass

#---------------------------------------------------------------------------------------------------

def check(abstract_constraints: set[str], derivation_tree) -> bool:
    pass

#---------------------------------------------------------------------------------------------------

def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:
    pass