import os
import mimetypes
import re
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from collections import defaultdict


class AnalysisModule:
    def __init__(self):
        # Initialize properties as needed
        self.file_sizes = defaultdict(int)
        self.file_types = defaultdict(int)
        self.folder_structure = defaultdict(list)
        self.functions_per_file = defaultdict(list)
        self.name = ''
        self.creator = ''
        self.purpose = ''

    def analyze_file(self, file_path):
        # Method to analyze each file
        """
        Analyzes a file and extracts various information.

        Args:
            file_path (str): The path of the file to be analyzed.

        Returns:
            None
        """
        # File size
        self.file_sizes[file_path] = os.path.getsize(file_path)

        # File type
        mime_type, _ = mimetypes.guess_type(file_path)
        self.file_types[mime_type] += 1

        # Functions in the file
        functions = self.extract_functions_from_file(file_path)
        self.functions_per_file[file_path] = functions

    def extract_functions_from_file(self, file_path):
        functions = []
        with open(file_path, 'r') as file:
            content = file.read()

            # Use regular expressions to find function definitions
            pattern = r'def\s+(\w+)\s*\('
            functions = re.findall(pattern, content)

        return functions

    def extract_additional_info(self, file_path):
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
                        self.name = match.group(1)
                    elif term == 'creator':
                        self.creator = match.group(1)
                    elif term == 'purpose':
                        self.purpose = match.group(1)

    def save_analysis_report(self, report_path):
        with open(report_path, 'w') as report_file:
            report_file.write("Application Analysis Report\n")
            report_file.write("=========================\n\n")

            # Overall statistics
            report_file.write(f"Total Files: {sum(len(files) for files in self.folder_structure.values())}\n")
            report_file.write(f"Total File Types: {len(self.file_types)}\n")
            report_file.write(f"Total Folder Structure: {len(self.folder_structure)} folders\n\n")

            # Additional information
            if self.name:
                report_file.write(f"Application Name: {self.name}\n")
            if self.creator:
                report_file.write(f"Creator: {self.creator}\n")
            if self.purpose:
                report_file.write(f"Purpose: {self.purpose}\n")

            # File Sizes
            report_file.write("\nFile Sizes:\n")
            for file_path, size in self.file_sizes.items():
                report_file.write(f"{file_path}: {size} bytes\n")

            # File Types
            report_file.write("\nFile Types:\n")
            for mime_type, count in self.file_types.items():
                report_file.write(f"{mime_type}: {count} files\n")

            # Folder Structure
            report_file.write("\nFolder Structure:\n")
            for folder, files in self.folder_structure.items():
                report_file.write(f"{folder}/ ({len(files)} files)\n")

            # Functions per File
            report_file.write("\nFunctions per File:\n")
            for file_path, functions in self.functions_per_file.items():
                report_file.write(f"{file_path}:\n")
                for func in functions:
                    report_file.write(f"  - {func}\n")

            # Additional Statistics (Future Enhancement)
            report_file.write("\nAdditional Statistics:\n")
            report_file.write(f"Average File Size: {self.calculate_average_file_size():.2f} bytes\n")
            report_file.write(f"Most Common File Type: {self.get_most_common_file_type()}\n")
            report_file.write(f"Number of Files in Each Folder:\n")
            for folder, files in self.folder_structure.items():
                report_file.write(f"{folder}: {len(files)} files\n")

    def generate_comprehensive_report(self):
        print("\nComprehensive Report:")
        print(f"Name: {self.name}")
        print(f"Creator: {self.creator}")
        print(f"Purpose: {self.purpose}")

        # Additional Visualizations (Future Enhancement)
        self.plot_additional_statistics()

    def analyze_application(self, folder_path, report_path=None):
        # Walk through the folder structure
        for root, dirs, files in os.walk(folder_path):
            relative_path = os.path.relpath(root, folder_path)
            self.folder_structure[relative_path].extend(files)

            for file in files:
                file_path = os.path.join(root, file)
                self.analyze_file(file_path)

                # Check if the file is a README or license file
                is_readme = re.match(r'readme', os.path.basename(file_path), re.IGNORECASE)
                is_license = re.match(r'license', os.path.basename(file_path), re.IGNORECASE)

                if is_readme or is_license:
                    self.extract_additional_info(file_path)

        # Save analysis to a report if specified
        if report_path:
            self.save_analysis_report(report_path)

        # Perform further analysis or generate insights as needed
        self.generate_comprehensive_report()

    # Additional Statistics (Future Enhancement)
    def calculate_average_file_size(self):
        total_size = sum(self.file_sizes.values())
        num_files = len(self.file_sizes)
        return total_size / num_files if num_files > 0 else 0

    def get_most_common_file_type(self):
        if self.file_types:
            return max(self.file_types, key=self.file_types.get)
        else:
            return "No file types found"

    # Additional Visualizations (Future Enhancement)
    def plot_additional_statistics(self):
        pass  # Placeholder for future visualization implementation


# Test the code
folder_path = "/home/nick/App_Lab_Analyzer"
analysis_module = AnalysisModule()
analysis_module.analyze_application(folder_path, report_path="analysis_report.txt")
