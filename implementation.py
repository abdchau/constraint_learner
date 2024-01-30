"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
from itertools import product
from fuzzingbook.Grammars import nonterminals
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer

from helpers import tree_to_string, get_all_subtrees
from timer import timer

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
    nts = set()
    timer.measure('Going to get subtrees')
    subtrees = get_all_subtrees(derivation_trees[0])
    timer.measure('Subtrees acquired. Gettings nts...')
    nts = set(subtrees.keys())
    
    for derivation_tree in derivation_trees[1:]:
        subtrees = get_all_subtrees(derivation_tree)
        nts.intersection_update(set(subtrees.keys()))
    
    nts = list(nts)
    timer.measure('NTs acquired.')


    # abstract constraints which hold for all derivation_trees
    result = set()

    timer.measure('Beginning work on constraint patterns')
    for constraint_pattern in constraint_patterns:
        timer.measure(f'Getting abstract constraints for {constraint_pattern}')
        abstract_constraints = instantiate_with_nonterminals(constraint_pattern, nts)
        timer.measure(f'{len(abstract_constraints)} abstract constraints acquired')
        
        timer.measure(f'Beginning evaluation of abstract constraints')
        for abstract_constraint in abstract_constraints:
            passed = False
        
            timer.measure(f'Evaluating one derivation tree')
            for derivation_tree in derivation_trees:
                chk = False
                try:
                    chk = check({abstract_constraint}, derivation_tree)
                except:
                    pass
                if not chk:
                    passed = False
                    break
                else:
                    passed = True
                    
            if passed:
                result.add(abstract_constraint)
            timer.measure(f'One derivation tree evaluated.')
        
        timer.measure(f'Done with abstract constraints for {constraint_pattern}\n')
                
    return result

#---------------------------------------------------------------------------------------------------

def check(abstract_constraints: set[str], derivation_tree) -> bool:
    nts_to_subtrees = get_all_subtrees(derivation_tree)
    
    passing_constraints = set()
    for abstract_constraint in abstract_constraints:
        if abstract_constraint in passing_constraints:
            continue

        concrete_constraints = instantiate_with_subtrees(abstract_constraint, nts_to_subtrees)
        for concrete_constraint in concrete_constraints:
            try:
                result = eval(concrete_constraint)
            except Exception as e:
                # print('Fail eval')
                raise e
            if result == True:
                passing_constraints.add(abstract_constraint)

    return len(passing_constraints) == len(abstract_constraints)

#---------------------------------------------------------------------------------------------------

def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:
    fuzzer = EvenFasterGrammarFuzzer(grammar)
    parser = EarleyParser(grammar)
    
    while True:
        fuzzed_input = fuzzer.fuzz()
        # valid_input = not produce_valid_sample
        valid_input = False

        try:
            valid_input = check(abstract_constraints, next(parser.parse(fuzzed_input)))
        except SyntaxError as e:
            pass

        if valid_input == produce_valid_sample:
            return fuzzed_input