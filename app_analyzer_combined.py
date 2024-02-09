#!/bin/bash

# run_analyzer.sh

# Define the path to the App_Lab_Analyzer script
APP_ANALYZER_SCRIPT="/home/nick/App_Lab_Analyzer/app_analyzer.py"
PRIVATE_GPT_DIRECTORY="/home/nick/PrivateGPT"

# Check if the input directory exists
if [ ! -d "$PRIVATE_GPT_DIRECTORY" ]; then
    echo "Error: PrivateGPT directory not found"
    exit 1
fi

# Run the app_analyzer.py script on the PrivateGPT directory
python3 $APP_ANALYZER_SCRIPT $PRIVATE_GPT_DIRECTORY

echo "Analysis completed on PrivateGPT directory"
# analysis_module.py

import os
import mimetypes
import re
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt

class AnalysisModule:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_sizes = {}
        self.file_types = {}
        self.functions_per_file = {}
        self.folder_structure = {}
        self.name = ''
        self.creator = ''
        self.purpose = ''

    def analyze(self):
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    file_type, _ = mimetypes.guess_type(file_path)
                    functions = self.extract_functions_from_file(file_path)

                    self.file_sizes[file_path] = file_size
                    self.file_types[file_path] = file_type
                    self.functions_per_file[file_path] = functions

                    folder = os.path.relpath(root, self.folder_path)
                    self.update_folder_structure(folder, file_path)

                    self.extract_additional_info(file_path)
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {e}")

    def extract_functions_from_file(self, file_path):
        functions = []
        with open(file_path, 'r') as file:
            content = file.read()
            pattern = r'def\s+(\w+)\s*\('
            functions = re.findall(pattern, content)

        return functions

    def extract_additional_info(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            search_terms = {
                'name': r'(?i)name:\s*(.*)',
                'creator': r'(?i)creator:\s*(.*)',
                'purpose': r'(?i)purpose:\s*(.*)',
            }

            for term, pattern in search_terms.items():
                match = re.search(pattern, content)
                if match:
                    setattr(self, term, match.group(1))

    def update_folder_structure(self, folder, file_path):
        if folder not in self.folder_structure:
            self.folder_structure[folder] = []
        self.folder_structure[folder].append(file_path)

    def app_insights(self):
        insights = "Overall Application Insights\n"
        insights += f"Average File Size: {self.calculate_average_file_size():.2f} bytes\n"
        insights += f"Most Common File Type: {self.get_most_common_file_type()}\n"
        insights += f"Number of Files in Each Folder:\n"
        for folder, files in self.folder_structure.items():
            insights += f"{folder}: {len(files)} files\n"

        return insights

    def calculate_average_file_size(self):
        if not self.file_sizes:
            return 0
        return sum(self.file_sizes.values()) / len(self.file_sizes)

    def get_most_common_file_type(self):
        if not self.file_types:
            return "No file types found"
        return max(self.file_types, key=self.file_types.get)

    def generate_comprehensive_report(self, data):
        try:
            df = pd.DataFrame(list(data.items()), columns=['Name', 'Value'])
            summary = df.describe()

            plt.bar(self.file_sizes.keys(), self.file_sizes.values())
            plt.title("File Sizes")
            plt.xlabel("File Path")
            plt.ylabel("Size (bytes)")
            plt.savefig("file_sizes_bar_chart.png")

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Comprehensive Report", ln=True, align='C')
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=f'Summary:\n{summary}\n\nBar Chart:\nSee attached image.', align='L')
            pdf.output("report.pdf")

            with open('report.pdf', 'rb') as f:
                report_content = f.read()

            return report_content
        except Exception as e:
            print(f"Error generating comprehensive report: {e}")
            return b''

    def iterate_for_insights(self):
        insights = ""

        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = self.file_sizes[file_path]
                file_type = self.file_types[file_path]
                functions = self.functions_per_file[file_path]

                file_insight = self.file_insights(file_path, file_size, file_type, functions)
                insights += file_insight

        return insights

    def file_insights(self, file_path, file_size, file_type, functions):
        insights = f"Insights for {file_path}\n"
        insights += f"Size: {file_size} bytes\n"
        insights += f"Type: {file_type}\n"

        insights += "Functions:\n"
        for func in functions:
            insights += f"  - {func}\n"

        return insights

    def combine_insights(self):
        try:
            self.analyze()  # Run analysis
            app_insights_info = self.app_insights()
            iterate_insights_info = self.iterate_for_insights()

            combined_insights = app_insights_info + iterate_insights_info

            report_data = {
                "Name 1": 10,
                "Name 2": 20,
                "Name 3": 30
            }
            comprehensive_report = self.generate_comprehensive_report(report_data)

            return combined_insights, comprehensive_report
        except Exception as e:
            print(f"Error combining insights: {e}")
            return "", b''

# test_analysis.py

from analysis_module import AnalysisModule

# Test the code
folder_path = "/home/nick/App_Lab_Analyzer"
analysis_module = AnalysisModule(folder_path)

combined_insights, comprehensive_report = analysis_module.combine_insights()

print(combined_insights)
# The comprehensive_report variable contains the content of the PDF report.
