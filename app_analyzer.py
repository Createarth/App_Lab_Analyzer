import os
import mimetypes
import re
from collections import defaultdict
from insights_module import AnalysisModule, combine_insights, perform_overall_analysis, generate_use_case_insights

def analyze_directory(directory_path):
    # Create an instance of the AnalysisModule
    analysis_module = AnalysisModule(directory_path)
    analysis_module.analyze()

    # Get insights from the AnalysisModule
    app_name = analysis_module.get_name()
    app_creator = analysis_module.get_creator()
    app_purpose = analysis_module.get_purpose()

    # Combine insights
    combined_insights, use_case_insights, comprehensive_report = combine_insights(
        app_name, app_creator, app_purpose, directory_path, analysis_module
    )

    # Print combined insights
    print("Combined Insights:")
    print(combined_insights)

    # Print use case insights
    print("\nUse Case Insights:")
    print(use_case_insights)

    # Save comprehensive report to file
    with open('comprehensive_report.txt', 'w') as report_file:
        report_file.write(comprehensive_report)

if __name__ == "__main__":
    directory_path = "/home/nick/App_Lab_Analyzer/privateGPT"
    analyze_directory(directory_path)

    # Continue with additional analysis and visualizations
    analyze_application(directory_path)

import os
import mimetypes
import re
from collections import defaultdict
from insights_module import AnalysisModule, combine_insights, perform_overall_analysis, generate_use_case_insights

def analyze_directory(directory_path):
    # Create an instance of the AnalysisModule
    analysis_module = AnalysisModule(directory_path)
    analysis_module.analyze()

    # Get insights from the AnalysisModule
    app_name = analysis_module.get_name()
    app_creator = analysis_module.get_creator()
    app_purpose = analysis_module.get_purpose()

    # Combine insights
    combined_insights, use_case_insights, comprehensive_report = combine_insights(
        app_name, app_creator, app_purpose, directory_path, analysis_module
    )

    # Print combined insights
    print("Combined Insights:")
    print(combined_insights)

    # Print use case insights
    print("\nUse Case Insights:")
    print(use_case_insights)

    # Save comprehensive report to file
    with open('comprehensive_report.txt', 'w') as report_file:
        report_file.write(comprehensive_report)

if __name__ == "__main__":
    directory_path = "/home/nick/App_Lab_Analyzer/privateGPT"
    analyze_directory(directory_path)

    # Continue with additional analysis and visualizations
    analyze_application(directory_path)
