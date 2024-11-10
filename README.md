Project: Integration and Storage Cost Calculation

This project processes linguistic data from a CSV file by applying a series of transformations and rules to calculate dependency distances and storage costs.
Steps

    Initial Cleaning: Removes prefixes from word IDs and preserves decimal formatting.
    Suffix Addition: Modifies the 4th column with word ID prefixes.
    Distance Calculation: Computes the distance between connected words based on index differences.
    Storage Cost Calculation: Applies custom rules to calculate storage costs based on dependency relations and POS tags.

Usage

Run the main script to process the data:

python script_name.py

The output will be saved as final_output.csv.

Ensure all input files (bhooki_check.csv) are in the same directory.
