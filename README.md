# IonForge

## What is it for?
This script serves to automatically generate Analytes for Qualitative Analysis lab courses in general introductory chemistry lab courses.
In this version it is designed for the module BCh1.2/2.1 for the Chemistry Bachelor Program of Bonn University.

## How it works
Each Analyte that needs to be analyzed by the students has a fixed pool of possible ions which can be included in the analyte.
From this pool of possible ions a random number is generated of how many ions are in the analysis and accordingly this many random picks
are done from the pool of ions. Then random picks from the pool of appropriate salts containing these ions are done.
This is done for each student individually.

## Usage
    python3 ion_distribution.py <student_names.csv> --probmode <probmode>