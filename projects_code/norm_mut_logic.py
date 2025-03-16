#!/bin/python

import sys

def parse_input(test_cases):
    """Parses input and separates it into NORM and MUT test cases."""
    norm_tests = []  # Stores NORM test cases
    mut_tests = []  # Stores MUT test cases

    for case in test_cases:
        genotype = case["type"]
        sample_ids = list(map(int, case["samples"]))

        if genotype == "NORM":
            norm_tests.append(sample_ids)
        else:
            mut_tests.append(sample_ids)

    return norm_tests, mut_tests  # Returns a tuple (List of NORM tests, List of MUT tests)
    

def process_norm_tests(norm_tests, sample_genotype, norm_samples):
    """Processes NORM test cases and marks all listed samples as NORM."""
    for sample_ids in norm_tests:  # Iterates over all NORM test cases
        for sample_id in sample_ids:  # Iterates over each sample ID in the test case
            sample_genotype[sample_id] = "NORM"  # Assigns "NORM" to each sample ID
            norm_samples.add(sample_id)  # Adds to the set of known NORM samples
        

def process_mut_tests(mut_tests, sample_genotype, norm_samples):
    """Processes MUT test cases to determine which are MUT, INCONSISTENT, or NONUNIQUE."""
    pending_mut_tests = mut_tests[:]  # Copy list for safer iteration
    changed = True  # A flag marker to track if updates happened
        
    while changed:  # Keeps processing as long as changes happen
        changed = False  # Reset flag for each loop iteration
        new_pending = []  # Stores unresolved MUT tests to recheck later
            
        for sample_ids in pending_mut_tests:  # Iterate over each MUT test
            known_normals = [s for s in sample_ids if s in norm_samples]  # Finds samples already marked as NORM
            unknowns = [s for s in sample_ids if s not in sample_genotype]  # Finds samples with unknown genotypes
                
            if len(unknowns) == 1:  # If exactly one sample is unknown, it must be MUT
                sample_genotype[unknowns[0]] = "MUT"
                changed = True  # Marks that an update happened
            elif len(unknowns) == 0:  # If all samples are already known
                if all(sample_genotype[s] == "NORM" for s in sample_ids):  # Check for contradiction
                    print("INCONSISTENT") 
                    return False  # Stops execution if an inconsistency is found
            else:
                new_pending.append(sample_ids)  # Keeps unresolved tests for next loop
        
    return True


def check_nonunique(mut_tests, sample_genotype):
    """Checks for multiple unknown sample IDs for NONUNIQUE after all processing (at the end)."""
    remaining_unknowns = set()  # Initializes remaining unknown set
    
    # Collects all remaining unknown samples after MUT processing is complete
    for sample_ids in mut_tests: 
        for sample_id in sample_ids:
            if sample_id not in sample_genotype:  # If a sample is still unknown
                remaining_unknowns.add(sample_id)  # Adds to remaining_unknowns
                
    if len(remaining_unknowns) > 1:  # If multiple unknowns remain
        print("NONUNIQUE") 
        return False  # Stops execution
        
    return True


def run_norm_mut_test(test_cases):
    """Runs the Norm vs. Mut test logic and returns results in a format Flask can use."""
    norm_tests, mut_tests = parse_input(test_cases)
    sample_genotype = {}  
    norm_samples = set()

    # Step 1: Process NORM test cases
    process_norm_tests(norm_tests, sample_genotype, norm_samples)

    # Step 2: Process MUT test cases
    if not process_mut_tests(mut_tests, sample_genotype, norm_samples):
        return {"error": "INCONSISTENT"}
    
    # Step 3: Check for NONUNIQUE errors
    if not check_nonunique(mut_tests, sample_genotype):
        return {"error": "NONUNIQUE"}

    # Step 4: Format and return results
    sorted_results = sorted(sample_genotype.items())
    return [{"sample_id": sid, "genotype": geno} for sid, geno in sorted_results]