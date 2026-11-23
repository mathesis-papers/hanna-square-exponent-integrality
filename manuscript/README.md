# Hanna's square-exponent factorial integrality conjectures

Haobo Ma — ChronoAI Pte Ltd, Singapore  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore

## Contents

- `note.tex`: self-contained mathematical proof and bibliography.
- `metadata.json`: bibliographic identity and license.
- `verify.py`: exact rational and integer coefficient calculations; Python 3.10 or later, standard library only.
- `verification.json`: the expected deterministic calculation output.

## Build

Compile with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, compile twice with a standard LaTeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; BibTeX and external figures are unnecessary.

## Exact finite calculations

```sh
python3 verify.py > calculated.json
cmp calculated.json verification.json
```

The script compares two coefficient constructions through degree 16 for all three series,
checks the defining equations, and compares all terms listed in the cited OEIS entries.
It also tests the divisibility lemma and additional cutoff choices over the finite ranges
specified in `verification.json`. All calculations use integers and exact fractions.
The all-degree conclusions follow from the written induction in the note, rather than from
the finite calculation ranges.
The additional checks compare 173 power-table coefficients in `source_examples.json`,
test homogeneous scaling for rational linear coefficients through degree 10,
and check the sharpness witnesses for degrees 1--48 and cutoffs 1--32.
The constant-cutoff-two example has fourth coefficient `211/2`.
The universal cancellation criterion is proved in the note; necessity of that
criterion for a particular recursively generated series is a different question.

## Formal statement

The pinned `.lean` source is linked in the note and in `metadata.json`.
Its `HannaSquareExponentIntegrality.result` declaration states existence, uniqueness
and integral coefficients for the three normalized series with cutoffs `n`, `n+1`,
and `2*n`. The general greatest-common-divisor criterion and arbitrary integer
linear coefficient are proved in the note, as are rational scaling and the
sharp universal cancellation criterion. The file's private `all_for_cutoff`
also covers mixtures of those three cutoffs, with linear coefficient 1.

## Sources and license

Paul D. Hanna posed the three integrality conjectures in OEIS A350410 and A350411
(revision 5) and A350412 (revision 9), each dated December 29, 2021.
The NAME and EXAMPLE sections fix the equations and initial coefficients.
The COMMENT sections state the conjectures.
The coefficient-divisibility tool is credited to Steffen Eger,
Journal of Integer Sequences 18 (2015), Article 15.4.1, Theorem 19;
the note includes a direct proof for signed integer coefficients.

Copyright 2026 Haobo Ma and Wenlin Zhang. CC BY 4.0 (`cc-by-4.0`).
The source archive contains the note, metadata, calculation script and its output.
It also contains the source-example data used by the calculation script.
OEIS source pages remain subject to their own terms.
