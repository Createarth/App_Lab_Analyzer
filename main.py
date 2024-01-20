import os
import mimetypes
import re
from collections import defaultdict
from analysis_module import perform_overall_analysis
from insights_module import generate_use_case_insights

def analyze_application(folder_path):
    # Initialize analysis variables
    file_sizes = defaultdict(int)
    file_types = defaultdict(int)
    folder_structure = defaultdict(list)
    functions_per_file = defaultdict(list)
    name = ''
    creator = ''
    purpose = ''

    # Function to analyze each file
    def analyze_file(file_path):
        """
        Analyzes a file and extracts various information.

        Args:
            file_path (str): The path of the file to be analyzed.

        Returns:
            None
        """
        # File size
        file_sizes[file_path] = os.path.getsize(file_path)

        # File type
        mime_type, _ = mimetypes.guess_type(file_path)
        file_types[mime_type] += 1

        # Functions in the file
        functions = extract_functions_from_file(file_path)
        functions_per_file[file_path] = functions

        # Check if the file is a README or license file
        is_readme = re.match(r'readme', os.path.basename(file_path), re.IGNORECASE)
        is_license = re.match(r'license', os.path.basename(file_path), re.IGNORECASE)

        if is_readme or is_license:
            extract_additional_info(file_path)

    # Function to extract functions from a file
    def extract_functions_from_file(file_path):
        functions = []
        with open(file_path, 'r') as file:
            content = file.read()

            # Use regular expressions to find function definitions
            pattern = r'def\s+(\w+)\s*\('
            functions = re.findall(pattern, content)

        return functions

    # Function to extract additional information from README or license files
    def extract_additional_info(file_path):
        nonlocal name, creator, purpose
        with open(file_path, 'r') as file:
            content = file.read()

            # Search for name, creator, and purpose information
            search_terms = {
                'name': r'(?i)name:\s*(.*)',
                'creator': r'(?i)creator:\s*(.*)',
                'purpose': r'(?i)purpose:\s*(.*)',
            }

            for term, pattern in search_terms.items():
                match = re.search(pattern, content)
                if match:
                    if term == 'name':
                        name = match.group(1)
                    elif term == 'creator':
                        creator = match.group(1)
                    elif term == 'purpose':
                        purpose = match.group(1)

    # Walk through the folder structure
    for root, dirs, files in os.walk(folder_path):
        relative_path = os.path.relpath(root, folder_path)
        folder_structure[relative_path].extend(files)

        for file in files:
            file_path = os.path.join(root, file)
            analyze_file(file_path)

    # Save analysis to a report
    report_path = os.path.join(folder_path, 'app_analysis_report.txt')
    with open(report_path, 'w') as report_file:
        report_file.write("Application Analysis Report\n")
        report_file.write("=========================\n\n")

        # Overall statistics
        report_file.write(f"Total Files: {sum(len(files) for files in folder_structure.values())}\n")
        report_file.write(f"Total File Types: {len(file_types)}\n")
        report_file.write(f"Total Folder Structure: {len(folder_structure)} folders\n\n")

        # Additional information
        if name:
            report_file.write(f"Application Name: {name}\n")
        if creator:
            report_file.write(f"Creator: {creator}\n")
        if purpose:
            report_file.write(f"Purpose: {purpose}\n")

        # File Sizes
        report_file.write("\nFile Sizes:\n")
        for file_path, size in file_sizes.items():
            report_file.write(f"{file_path}: {size} bytes\n")

        # File Types
        report_file.write("\nFile Types:\n")
        for mime_type, count in file_types.items():
            report_file.write(f"{mime_type}: {count} files\n")

        # Folder Structure
        report_file.write("\nFolder Structure:\n")
        for folder, files in folder_structure.items():
            report_file.write(f"{folder}/ ({len(files)} files)\n")

        # Functions per File
        report_file.write("\nFunctions per File:\n")
        for file_path, functions in functions_per_file.items():
            report_file.write(f"{file_path}:\n")
            for func in functions:
                report_file.write(f"  - {func}\n")

    print(f"Analysis report saved to {report_path}")

    # Perform further analysis using the extracted information
    perform_overall_analysis(name, creator, purpose)

    # Generate use case insights
    generate_use_case_insights(folder_structure, functions_per_file)

    # Sort use cases by number of keyword matches
    sorted_use_cases = sorted(use_case_matches.items(), key=lambda item: item[1], reverse=True)

    # Generate visual representation of directory structure
    print("\nVisual Representation of Directory Structure:")
    for root, dirs, files in os.walk(folder_path):
        level = root.replace(folder_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(sub_indent, f))

    # Print the most likely use cases
    print("\nPotential Use Cases:")
    for use_case, matches in sorted_use_cases:
        if matches > 0:
            print(f"{use_case}: {matches} matches")

    # Print comprehensive report and analysis including all of the information obtained.
    print("\nComprehensive Report:")
    print(f"Name: {name}")
    print(f"Creator: {creator}")
    print(f"Purpose: {purpose}")
    print("\nFile Sizes:")
    for file_path, size in file_sizes.items():
        print(f"{file_path}: {size} bytes")

# Add this line at the end of the analyze_application function
folder_structure = ...
functions_per_file = ...
use_case_matches = ...

# Example usage:
analyze_application(r'I:\Createarth\Document_Analysis_ML')
