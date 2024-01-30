import re
import mimetypes
import os

class AnalysisModule:
    def __init__(self):
        self.file_sizes = {}
        self.file_types = {}
        self.folder_structure = {}
        self.functions_per_file = {}
        self.name = None
        self.creator = None
        self.purpose = None

    def extract_additional_info(self, content):
        # Extract application name, creator, and purpose from README or license files
        patterns = {'name': r'name\s*:\s*(\w+)', 'creator': r'creator\s*:\s*(\w+)', 'purpose': r'purpose\s*:\s*(\w+)'}
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                setattr(self, key, match.group(1))

    def analyze_file(self, filename):
        # Analyze file and extract information
        size = os.path.getsize(filename)
        self.file_sizes[filename] = size

        file_type, _ = mimetypes.guess_type(filename)
        self.file_types[filename] = file_type

        with open(filename, 'r') as file:
            content = file.read()

            # Extract additional information from README or license files
            if 'README' in filename.upper() or 'LICENSE' in filename.upper():
                self.extract_additional_info(content)

            # Extract functions from files using regular expressions
            functions = re.findall(r'def\s+(\w+)\s*\(', content)
            self.functions_per_file[filename] = functions

    def analyze_folder_structure(self, root_folder):
        # Analyze folder structure and count occurrences
        for foldername, _, filenames in os.walk(root_folder):
            folder_parts = foldername.split(os.path.sep)
            current_folder = self.folder_structure
            for part in folder_parts:
                current_folder = current_folder.setdefault(part, {})
            for filename in filenames:
                current_folder[filename] = None

    def calculate_average_file_size(self):
        # Calculate the average file size
        total_size = sum(self.file_sizes.values())
        num_files = len(self.file_sizes)
        return total_size / num_files if num_files > 0 else 0

def analyze_static_code_analysis_tools():
    # Create an instance of the AnalysisModule class
    analysis_module = AnalysisModule()

    # Analyze each static code analysis tool based on the provided prompts
    analysis_module.analyze_file('AdaControl.txt')
    analysis_module.analyze_file('Axivion_Bauhaus_Suite.txt')
    analysis_module.analyze_file('BLAST.txt')
    analysis_module.analyze_file('Clang.txt')
    analysis_module.analyze_file('Coccinelle.txt')
    analysis_module.analyze_file('CodeDx.txt')
    analysis_module.analyze_file('CodePeer.txt')
    analysis_module.analyze_file('CodeRush.txt')
    analysis_module.analyze_file('CodeScene.txt')
    analysis_module.analyze_file('CodeQL.txt')

    # Analyze the folder structure of the tools
    analysis_module.analyze_folder_structure('tools_folder')

    # Calculate the average file size
    average_file_size = analysis_module.calculate_average_file_size()

    # Generate a comprehensive report
    report = {
        'Name': analysis_module.name,
        'Creator': analysis_module.creator,
        'Purpose': analysis_module.purpose,
        'File Sizes': analysis_module.file_sizes,
        'File Types': analysis_module.file_types,
        'Average File Size': average_file_size,
        'Folder Structure': analysis_module.folder_structure,
        'Functions per File': analysis_module.functions_per_file
    }

    return report

# Execute the analysis and print the report
analysis_report = analyze_static_code_analysis_tools()
print(analysis_report)
