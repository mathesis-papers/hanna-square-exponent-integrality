import json
from fractions import Fraction
from math import comb, factorial, gcd
from pathlib import Path


def multiply(left, right, degree):
    product = [0] * (degree + 1)
    for left_degree, left_value in enumerate(left[: degree + 1]):
        for right_degree, right_value in enumerate(right[: degree - left_degree + 1]):
            product[left_degree + right_degree] += left_value * right_value
    return product


def binary_power(polynomial, exponent, degree):
    result = [1] + [0] * degree
    factor = polynomial[: degree + 1] + [0] * max(0, degree + 1 - len(polynomial))
    while exponent:
        if exponent % 2:
            result = multiply(result, factor, degree)
        exponent //= 2
        if exponent:
            factor = multiply(factor, factor, degree)
    return result


def rational_next(prefix, cutoff):
    degree = len(prefix)
    positive_part = [0] + prefix[1:]
    powers = [[1] + [0] * degree]
    for order in range(1, degree + 1):
        powers.append(multiply(powers[-1], positive_part, degree))
    constant = Fraction(0)
    slope = Fraction(0)
    for index in range(cutoff + 1):
        exponent = index * index
        coefficient = sum(
            (-1) ** (exponent + order) * comb(exponent, order) * powers[order][degree]
            for order in range(min(exponent, degree) + 1)
        )
        constant += Fraction(coefficient, factorial(index))
        if index:
            slope += Fraction((-1) ** (index - 1) * exponent, factorial(index))
    assert slope == Fraction((-1) ** (cutoff - 1), factorial(cutoff - 1))
    return -constant / slope


def integer_next(prefix, cutoff):
    degree = len(prefix)
    coefficients = [
        binary_power(prefix, index * index, degree)[degree]
        for index in range(cutoff + 1)
    ]
    assert coefficients[-1] % cutoff == 0
    cleared = sum(
        factorial(cutoff - 1) // factorial(index) * coefficients[index]
        for index in range(cutoff)
    ) + coefficients[-1] // cutoff
    return (-1) ** cutoff * cleared


def construct(cutoff_function, degree, linear=1):
    rational = [Fraction(-1), Fraction(linear)]
    integral = [-1, linear]
    for index in range(2, degree + 1):
        cutoff = cutoff_function(index)
        assert cutoff >= 1 and cutoff % gcd(index, cutoff * cutoff) == 0
        rational.append(rational_next(rational, cutoff))
        integral.append(integer_next(integral, cutoff))
        assert rational[-1].denominator == 1
        assert rational[-1] == integral[-1]
    equations = 0
    for index in range(2, degree + 1):
        cutoff = cutoff_function(index)
        equation = sum(
            Fraction(binary_power(integral, term * term, index)[index], factorial(term))
            for term in range(cutoff + 1)
        )
        assert equation == 0
        equations += 1
    return integral, equations


def rational_construct(cutoff_function, degree, linear):
    coefficients = [Fraction(-1), Fraction(linear)]
    for index in range(2, degree + 1):
        cutoff = cutoff_function(index)
        coefficients.append(rational_next(coefficients, cutoff))
        equation = sum(
            Fraction(binary_power(coefficients, term * term, index)[index], factorial(term))
            for term in range(cutoff + 1)
        )
        assert equation == 0
    return coefficients


def prime_factors(value):
    candidate = 2
    factors = []
    while candidate * candidate <= value:
        exponent = 0
        while value % candidate == 0:
            value //= candidate
            exponent += 1
        if exponent:
            factors.append((candidate, exponent))
        candidate += 1
    if value > 1:
        factors.append((value, 1))
    return factors


def valuation(value, prime):
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def main():
    expected = {
        'A350410': [-1, 1, 3, 12, 116, -534, -19083, 4653416, 8687989872,
                    -128647855586426, -17178731504646708274,
                    22932060477876906089601744,
                    336748983792218322012229442319058,
                    -59340140012235302782558826850918965528904,
                    -135935979554634873389993183019614435570206186506348,
                    4359616519227623971178976912185258573259921937219097427608884],
        'A350411': [-1, 1, 6, 76, 74, 26058, -7794632, -14388774920,
                    213380711849598, 28487519401892735386,
                    -38029127603565193657832846,
                    -558442679082054075230555562505128,
                    98405860538000983882824515617294391388622,
                    225427456282611271896161167867656072505435638401710],
        'A350412': [1, 12, 830, 1867901, 251714851830, 3696867014099083814,
                    8468768030682252554158546818,
                    4074040763513889480730186336041282515610,
                    533088609878310228401628064629048305794583364205468626,
                    23856105278172150534783174192628043609641782797360374708050534816035626]
    }
    cutoffs = {
        'A350410': lambda degree: degree,
        'A350411': lambda degree: degree + 1,
        'A350412': lambda degree: 2 * degree
    }
    sources = {
        'A350410': {'revision': 5, 'offset': 0},
        'A350411': {'revision': 5, 'offset': 0},
        'A350412': {'revision': 9, 'offset': 1}
    }
    series = {}
    equation_count = 0
    term_count = 0
    for name, cutoff in cutoffs.items():
        coefficients, count = construct(cutoff, 16)
        equation_count += count
        listed = coefficients[1:] if name == 'A350412' else coefficients
        assert listed[:len(expected[name])] == expected[name]
        term_count += len(expected[name])
        if name == 'A350412':
            coefficients[0] += 1
        series[name] = coefficients
    slope_count = 0
    for cutoff in range(1, 65):
        total = sum(Fraction((-1) ** (index - 1) * index * index, factorial(index))
                    for index in range(1, cutoff + 1))
        assert total == Fraction((-1) ** (cutoff - 1), factorial(cutoff - 1))
        slope_count += 1
    samples = [[-1, 1, 2, -3], [2, -3, 0, 1], [0, 1, -1, 2], [1], [-1, 0, 5]]
    divisor_count = 0
    last_term_count = 0
    for polynomial in samples:
        for exponent in range(1, 31):
            coefficients = binary_power(polynomial, exponent, 12)
            for degree in range(1, 13):
                assert coefficients[degree] % (exponent // gcd(degree, exponent)) == 0
                divisor_count += 1
        for cutoff in range(1, 25):
            coefficients = binary_power(polynomial, cutoff * cutoff, 12)
            for degree in range(1, 13):
                if cutoff % gcd(degree, cutoff * cutoff) == 0:
                    assert coefficients[degree] % cutoff == 0
                    last_term_count += 1
    additional = {
        'triple_degree': lambda degree: 3 * degree,
        'coprime': lambda degree: next(candidate for candidate in range(degree + 3, 2 * degree + 4)
                                         if gcd(degree, candidate) == 1),
        'mixed': lambda degree: [degree, degree + 1, 2 * degree][degree % 3],
        'smallest_admissible_at_least_four': lambda degree: next(
            candidate for candidate in range(4, 2 * degree + 5)
            if candidate % gcd(degree, candidate * candidate) == 0)
    }
    additional_equations = 0
    for cutoff in additional.values():
        for linear in [-2, 0, 1, 3]:
            _, count = construct(cutoff, 12, linear)
            additional_equations += count
    source_examples = json.loads(Path(__file__).with_name('source_examples.json').read_text())
    example_count = 0
    for name, rows in source_examples['tables'].items():
        normalized = series[name][:]
        if name == 'A350412':
            normalized[0] -= 1
        for row in rows:
            values = row['coefficients']
            actual = binary_power(normalized, row['power_index'] ** 2, len(values) - 1)
            assert actual == values
            example_count += len(values)
    scaling_cutoffs = {**cutoffs, 'mixed': additional['mixed']}
    scaling_linears = [Fraction(-2), Fraction(0), Fraction(3), Fraction(1, 2), Fraction(-2, 3)]
    scaling_count = 0
    for cutoff in scaling_cutoffs.values():
        base = rational_construct(cutoff, 10, 1)
        for linear in scaling_linears:
            scaled = rational_construct(cutoff, 10, linear)
            for degree in range(11):
                assert scaled[degree] == base[degree] * linear ** degree
                scaling_count += 1
    sharpness_count = 0
    criterion_count = 0
    witness_examples = []
    for degree in range(1, 49):
        for cutoff in range(1, 33):
            condition = cutoff % gcd(degree, cutoff * cutoff) == 0
            factors = prime_factors(cutoff)
            assert condition == all(valuation(degree, prime) <= exponent
                                    for prime, exponent in factors)
            criterion_count += 1
            if condition:
                continue
            prime, exponent = next((prime, exponent) for prime, exponent in factors
                                   if valuation(degree, prime) > exponent)
            order = prime ** (exponent + 1)
            assert degree % order == 0
            coefficient = (-1) ** (cutoff * cutoff - order) * comb(cutoff * cutoff, order)
            assert valuation(abs(coefficient), prime) == exponent - 1
            assert coefficient % cutoff != 0
            sharpness_count += 1
            if len(witness_examples) < 8:
                witness_examples.append({'degree': degree, 'cutoff': cutoff,
                                         'prime': prime, 'polynomial_monomial_degree': degree // order,
                                         'coefficient': coefficient})
    obstruction = rational_construct(lambda degree: 2, 4, 1)
    assert obstruction == [Fraction(-1), Fraction(1), Fraction(3), Fraction(16), Fraction(211, 2)]
    result = {
        'arithmetic': 'Exact Python integers and fractions.Fraction; no numerical rounding.',
        'series_degree_range': [0, 16],
        'defining_equations_degree_range': [2, 16],
        'defining_equations_checked': equation_count,
        'listed_oeis_terms_matched': term_count,
        'sources': sources,
        'series': series,
        'slope_cutoff_range': [1, 64],
        'slope_identities_checked': slope_count,
        'divisibility_samples': samples,
        'divisibility_degree_range': [1, 12],
        'divisibility_exponent_range': [1, 30],
        'divisibility_checks': divisor_count,
        'last_term_cutoff_range': [1, 24],
        'last_term_checks': last_term_count,
        'additional_cutoffs': list(additional),
        'additional_linear_coefficients': [-2, 0, 1, 3],
        'additional_degree_range': [2, 12],
        'additional_equations_checked': additional_equations,
        'source_example_coefficients_matched': example_count,
        'scaling_degree_range': [0, 10],
        'scaling_linear_coefficients': [str(value) for value in scaling_linears],
        'scaling_cutoffs': list(scaling_cutoffs),
        'scaling_coefficients_checked': scaling_count,
        'sharpness_degree_range': [1, 48],
        'sharpness_cutoff_range': [1, 32],
        'primewise_criterion_pairs_checked': criterion_count,
        'sharpness_witnesses_checked': sharpness_count,
        'sharpness_witness_examples': witness_examples,
        'constant_cutoff_two_coefficients_through_degree_four': [str(value) for value in obstruction],
        'A350412_positive_coefficients_checked': [1, 16],
        'construction_agreement': 'Rational binomial expansion agrees with integer binary-power cancellation.',
        'scope': 'Finite exact calculations; existence, uniqueness, integrality, scaling and universal cancellation follow in all degrees from the written proofs in note.tex.'
    }
    assert all(coefficient > 0 for coefficient in series['A350412'][1:])
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
