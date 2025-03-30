# This is a program to automatically assign ions that are contained in a 
# "Ursubstanz" which is given to the students. By means of qualitative
# analysis, the students have to identify the ions in the solution.
# In total the students will have to analyse 13 different analytes.
# Each analyte has a different list of possible cations and anions.
# The program randomly selects a number of cations and anions from the lists
# and assigns them to the analyte.
# The list of students is read in from a csv file.
# The program then creates a new csv file with the names of the students
# and the ions that are assigned to them.

import random
import pandas as pd
import sys
import os
import argparse

# list of ions analyte 1: easy anions
analyte_1_anions = ['Cl-', 'Br-', 'I-', 'NO3-', 'SO4--', 'CO3--', 'PO4---', 'S--']
analyte_1_cations = []

# list of ions analyte 2: difficult anions
analyte_2_anions = ['F-', 'SO3--', 'S2O3--', 'SCN-', 'NO2-', 'C2O4--', 'H3C2O2-', 'SiO4----', 'BO3---']
analyte_2_cations = []

# list of ions analyte 3: full anion analysis
analyte_3_anions = analyte_1_anions + analyte_2_anions
analyte_3_cations = []

# list of ions analyte 4: cations of soluble salts annd ammoniumcarbonate group
analyte_4_anions = analyte_1_anions
analyte_4_cations = ['Li+', 'Na+', 'K+', 'NH4+', 'Mg++', 'Ca++', 'Sr++', 'Ba++']

# list of ions analyte 5: small full analysis
analyte_5_anions = analyte_3_anions
analyte_5_cations = analyte_4_cations

# list of ions analyte 6: cations of urotropine group
analyte_6_anions = ['Cl-', 'NO3-', 'SO4--', 'CO3--', 'PO4---', 'S--']
analyte_6_cations = ['Fe+++', 'Al+++', 'Cr+++', 'TiO++']

# list of ions analyte 7: cations of urotropine group and ammoniumsulfide group
analyte_7_anions = analyte_6_anions
analyte_7_cations = analyte_6_cations + ['Mn++', 'Ni++', 'Co++', 'Zn++']

# list of ions analyte 8: Hydrogen sulfide group
analyte_8_anions = analyte_1_anions
analyte_8_cations = ['As+++', 'As+++++', 'Sb+++', 'Sb+++++', 'Sn++', 'Sn++++', 'Hg++', 'Pb++', 'Bi+++', 'Cu++', 'Cd++']

# list of ions analyte 9: small full analysis
analyte_9_anions = analyte_1_anions
analyte_9_cations = analyte_4_cations + analyte_7_cations + analyte_8_cations

# list of ions analyte 10: rare elements
analyte_10_anions = ['Cl-', 'NO3-', 'SO4--', 'CO3--']
analyte_10_cations = ['Ag+', 'W++++++', 'Se++++', 'Se++++++', 'Te++++', 'Te++++++', 'Ge++++', 'Tl+', 'ZrO++', 'Ce+++', 'Ce++++', 'V+++', 'V++++', 'V+++++', 'Cs+']

# list of ions analyte 11: big full analysis
analyte_11_anions = analyte_3_anions + ['[Fe(CN)6]3-', '[Fe(CN)6]4-']
analyte_11_cations = analyte_9_cations + analyte_10_cations

# list of ions analyte 12: big full analysis
analyte_12_anions = analyte_11_anions 
analyte_12_cations = analyte_11_cations

# list of ions analyte 13: spectroscopy
analyte_13_anions = analyte_1_anions
analyte_13_cations = ['Li+', 'Na+', 'K+', 'Cs+', 'Ca++', 'Sr++', 'Ba++', 'Tl+']

# Here is a list of all possible salts which contain the ions
# The salts are assigned the ions that are contained in the salt

possible_salts = {
    'Cl-': ['AgCl', 'Hg2Cl2', 'PbCl2', 'CuCl2', 'ZnCl2', 'CdCl2'],
    'Br-': ['AgBr', 'Hg2Br2', 'PbBr2', 'CuBr2', 'ZnBr2', 'CdBr2'],
    'I-': ['AgI', 'Hg2I2', 'PbI2', 'CuI2', 'ZnI2', 'CdI2'],
    'NO3-': ['AgNO3', 'Hg2(NO3)2', 'Pb(NO3)2', 'Cu(NO3)2', 'Zn(NO3)2', 'Cd(NO3)2'],
    'SO4--': ['Ag2SO4', 'Hg2SO4', 'PbSO4', 'CuSO4', 'ZnSO4', 'CdSO4'],
    'CO3--': ['Ag2CO3', 'Hg2CO3', 'PbCO3', 'CuCO3', 'ZnCO3', 'CdCO3'],
    'PO4---': ['Ag3PO4', 'Hg3(PO4)2', 'Pb3(PO4)2', 'Cu3(PO4)2', 'Zn3(PO4)2', 'Cd3(PO4)2'],
    # add more salts as needed
}

def print_header():
    print("=" * 80)
    print("                                                                     ")                                   
    print("     ██╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██████╗  ██████╗ ███████╗")
    print("     ██║██╔═══██╗████╗  ██║██╔════╝██║═══██║██╔══██╗██╔════╝ ██╔════╝")
    print("     ██║██║   ██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║  ███╗█████╗  ")
    print("     ██║██║   ██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  ")
    print("     ██║╚██████╔╝██║ ╚████║██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗")
    print("     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝")
    print("                                                                     ")
    print("                      Ion Distribution Program                       ")
    print("                      Author: Christian Selzer                       ")
    print("                      Version: 1.0                                   ")
    print("                      University of Bonn                             ")
    print("                      Department of Chemistry                        ")
    print("                                                                     ")
    print("=" * 80)

def main():
    # Print a nice header to the console
    print_header()
    # Read in the list of students from the csv file
    print("Reading in the list of students from the csv file...")
    student_df, args = input()
    print("Done reading in the list of students.")
    # Create a new dataframe to store the results, it is the same as the input dataframe with the columns "Cations", "Anions" and "Salts" added
    result_df = student_df.copy()

    print("Assigning ions to the students...")
    # Loop through the students and assign ions to them
    for index, row in student_df.iterrows():
        for analyte in range(1, 14):
            # Create a dictionary to store the analyte information
            analyte_dict = {}
            analyte_dict['anions'] = eval(f'analyte_{analyte}_anions')
            # Check if the analyte has cations
            analyte_dict['cations'] = eval(f'analyte_{analyte}_cations')
            # Assign ions to the student
            ions = assign_ions(analyte, analyte_dict, args)
            # Assign salts to the ions
            salts = assign_salts(ions)
            # Add the results to the dataframe
            result_df.at[index, f'Analyte{analyte}Cations'] = ', '.join([ion for ion in ions if ion in analyte_dict['cations']])
            result_df.at[index, f'Analyte{analyte}Anions'] = ', '.join([ion for ion in ions if ion in analyte_dict['anions']])
            result_df.at[index, f'Analyte{analyte}Salts'] = ', '.join(set(salt for ion in ions for salt in salts[ion]))
    
    print("Done assigning ions to the students.")
    # Save the results to a new csv file
    output_file = os.path.splitext(args.csv_file)[0] + '_assigned_ions.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

def assign_ions(analyte_number, analyte, args):
    # Define the number of cations and anions to select
    # get a random number between 1 and the length of the list

    # the probability follows a gaussian distribution

    if args.probmode == 'gaussian':
        # Use Gaussian distribution to determine the number of cations and anions
        num_cations = max(1, min(len(analyte['cations']), int(random.gauss(len(analyte['cations']) / 2, len(analyte['cations']) / 6))))
        num_anions = max(1, min(len(analyte['anions']), int(random.gauss(len(analyte['anions']) / 2, len(analyte['anions']) / 6))))

    elif args.probmode == 'uniform':
        # Use uniform distribution to determine the number of cations and anions
        num_cations = random.randint(1, len(analyte['cations']))
        num_anions = random.randint(1, len(analyte['anions']))
        
    # Select random cations and anions from the respective lists
    if analyte_number > 3:
        cations = random.sample(analyte['cations'], num_cations)
    else:
        cations = []
    anions = random.sample(analyte['anions'], num_anions)

    # Combine the selected cations and anions into a single list
    return cations + anions

def assign_salts(ions):

    salts = {}
    for ion in ions:
        # Check if the ion is in the possible_salts dictionary
        if ion in possible_salts:
            # Assign a random salt to the ion
            salts[ion] = [random.choice(possible_salts[ion])]
        else:
            # If no salts are found, assign an empty list
            salts[ion] = []
    return salts

def input():
    # Check if a command-line argument is provided
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Ion Distribution Program")
    parser.add_argument('csv_file', nargs='?', default=os.path.join(os.path.dirname(__file__), 'names.csv'),
                        help="Path to the CSV file containing the list of students (default: 'names.csv').")
    parser.add_argument('--probmode', choices=['gaussian', 'uniform'], default='gaussian',
                        help="Probability mode for ion selection (default: 'gaussian').")

    # Parse arguments
    args = parser.parse_args()

    # Check if the file exists
    if not os.path.exists(args.csv_file):
        print(f"Error: The file '{args.csv_file}' does not exist.")
        sys.exit(1)

    # Read in the list of students from the csv file
    df = pd.read_csv(args.csv_file, sep=',')
    return df, args

if __name__ == '__main__':
    # Call the main function
    main()