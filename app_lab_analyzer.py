import os
import mimetypes
import re
from collections import defaultdict
from analysis_module import AnalysisModule, perform_overall_analysis
from insights_module import combine_insights, generate_use_case_insights

def analyze_application(folder_path):
    # Create an instance of the AnalysisModule
    analysis_module = AnalysisModule()

    # Initialize additional variables
    file_sizes = defaultdict(int)
    file_types = defaultdict(int)
    folder_structure = defaultdict(list)
    functions_per_file = defaultdict(list)
    name = ''
    creator = ''
    purpose = ''
    use_case_matches = defaultdict(int)  # Initialize use_case_matches

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
        functions = analysis_module.extract_functions_from_file(file_path)
        functions_per_file[file_path] = functions

        # Check if the file is a README or license file
        is_readme = re.match(r'readme', os.path.basename(file_path), re.IGNORECASE)
        is_license = re.match(r'license', os.path.basename(file_path), re.IGNORECASE)

        if is_readme or is_license:
            analysis_module.extract_additional_info(file_path)

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
        if analysis_module.name:
            report_file.write(f"Application Name: {analysis_module.name}\n")
        if analysis_module.creator:
            report_file.write(f"Creator: {analysis_module.creator}\n")
        if analysis_module.purpose:
            report_file.write(f"Purpose: {analysis_module.purpose}\n")

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
    perform_overall_analysis(analysis_module.name, analysis_module.creator, analysis_module.purpose)

    # Generate use case insights
    use_case_matches = generate_use_case_insights(folder_structure, functions_per_file)

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
    print(f"Name: {analysis_module.name}")
    print(f"Creator: {analysis_module.creator}")
    print(f"Purpose: {analysis_module.purpose}")

    # Add this line at the end of the analyze_application function
    folder_structure = analysis_module.folder_structure
    functions_per_file = analysis_module.functions_per_file
    use_case_matches = use_case_matches

# Example usage:
analyze_application(r'I:\Createarth\Document_Analysis_ML')
