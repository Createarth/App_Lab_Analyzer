import os
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF  # Added for PDF report generation

import os
import mimetypes
import re
from collections import defaultdict

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
        # Analyze the folder structure and collect information about each file
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Extract information from the file
                file_size = os.path.getsize(file_path)
                file_type, _ = mimetypes.guess_type(file_path)
                functions = self.extract_functions_from_file(file_path)
                # Update the properties of the AnalysisModule instance
                self.file_sizes[file_path] = file_size
                self.file_types[file_path] = file_type
                self.functions_per_file[file_path] = functions
                # Update the folder structure
                folder = os.path.relpath(root, self.folder_path)
                if folder not in self.folder_structure:
                    self.folder_structure[folder] = []
                self.folder_structure[folder].append(file_path)

                # Extract additional information from files
                self.extract_additional_info(file_path)

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

    def get_file_sizes(self):
        return self.file_sizes

    def get_file_types(self):
        return self.file_types

    def get_functions_per_file(self):
        return self.functions_per_file

    def get_folder_structure(self):
        return self.folder_structure

    def get_name(self):
        return self.name

    def get_creator(self):
        return self.creator

    def get_purpose(self):
        return self.purpose

def app_insight(name, creator, purpose):
    """
    Generate insights based on application details.

    Args:
        name (str): The name of the application.
        creator (str): The creator or author of the application.
        purpose (str): The purpose or intended use of the application.

    Returns:
        str: Insights based on the provided details.
    """
    # Customize the insights generation based on your requirements
    insights = f"Insights for {name}\n"
    insights += f"Created by {creator}\n"
    insights += f"Purpose: {purpose}\n"

    # Add more insights based on your analysis

    return insights

def app_insights(folder_structure, functions_per_file, file_sizes, file_types):
    """
    Generate insights based on overall application analysis.

    Args:
        folder_structure (dict): Folder structure information.
        functions_per_file (dict): Functions per file information.
        file_sizes (dict): File sizes information.
        file_types (dict): File types information.

    Returns:
        str: Overall insights based on the analysis.
    """
    # Customize the insights generation based on your requirements
    insights = "Overall Application Insights\n"

    # Additional Statistics (Future Enhancement)
    insights += f"Average File Size: {calculate_average_file_size(file_sizes):.2f} bytes\n"
    insights += f"Most Common File Type: {get_most_common_file_type(file_types)}\n"
    insights += f"Number of Files in Each Folder:\n"
    for folder, files in folder_structure.items():
        insights += f"{folder}: {len(files)} files\n"

    # Add more insights based on folder structure and functions per file

    return insights

def file_insights(file_path, file_size, file_type, functions):
    """
    Generate insights for an individual file.

    Args:
        file_path (str): The path of the file.
        file_size (int): The size of the file in bytes.
        file_type (str): The type or MIME type of the file.
        functions (list): List of functions in the file.

    Returns:
        str: Insights for the individual file.
    """
    # Customize the insights generation based on your requirements
    insights = f"Insights for {file_path}\n"
    insights += f"Size: {file_size} bytes\n"
    insights += f"Type: {file_type}\n"

    # Add insights based on functions in the file

    return insights

def calculate_average_file_size(file_sizes):
    if not file_sizes:
        return 0
    return sum(file_sizes.values()) / len(file_sizes)

def get_most_common_file_type(file_types):
    if not file_types:
        return "No file types found"
    return max(file_types, key=file_types.get)

def generate_comprehensive_report(data):
    """
    Generate a comprehensive report based on the provided data.

    Args:
        data (pd.DataFrame): The data to be analyzed.

    Returns:
        bytes: The content of the comprehensive report in PDF format.
    """
    # Generate a summary of the data
    summary = data.describe()

    # Create a bar chart of the data
    data.plot(kind='bar', x='Name', y='Value')
    
    # Save the report to a PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Comprehensive Report", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f'Summary:\n{summary}\n\nBar Chart:\nSee attached image.', align='L')
    pdf.output("report.pdf")

    # Return the content of the PDF report
    with open('report.pdf', 'rb') as f:
        report_content = f.read()

    return report_content

def iterate_for_insights(folder_path, analysis_module):
    """
    Iterate through the folder structure and generate insights.

    Args:
        folder_path (str): The path of the application folder.
        analysis_module (AnalysisModule): An instance of the AnalysisModule.

    Returns:
        str: Insights generated for the entire application.
    """
    # Initialize insights variables
    insights = ""

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Extract information from the AnalysisModule instance
            file_size = analysis_module.file_sizes[file_path]
            file_type = analysis_module.file_types[file_path]
            functions = analysis_module.functions_per_file[file_path]
            # Generate insights for the file
            file_insight = file_insights(file_path, file_size, file_type, functions)
            insights += file_insight

    return insights

def generate_use_case_insights(folder_structure, functions_per_file):
    # Define your logic for generating use case insights
    return "Use case insights go here"

def combine_insights(name, creator, purpose, folder_path, analysis_module):
    """
    Generate combined insights and use case insights.

    Args:
        name (str): The name of the application.
        creator (str): The creator or author of the application.
        purpose (str): The purpose or intended use of the application.
        folder_path (str): The path to the folder to be analyzed.
        analysis_module (AnalysisModule): The analysis module to be used.

    Returns:
        tuple: Combined insights, use case insights, and the report.
    """
    # Generate application insights
    app_insight_info = app_insight(name, creator, purpose)
    
    # Generate overall application insights
    app_insights_info = app_insights(
        analysis_module.folder_structure,
        analysis_module.functions_per_file,
        analysis_module.file_sizes,
        analysis_module.file_types
    )
    
    # Iterate through the folder structure and generate insights
    iterate_insights_info = iterate_for_insights(folder_path, analysis_module)
    
    # Combine all insights
    combined_insights = app_insight_info + app_insights_info + iterate_insights_info
    
    # Generate use case insights (customize this part based on your requirements)
    use_case_insights = generate_use_case_insights(
        analysis_module.folder_structure,
        analysis_module.functions_per_file
    )
    
    return combined_insights, use_case_insights, generate_comprehensive_report(analysis_module.get_file_sizes())
