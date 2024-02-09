# app_lab_analysis.py

import os
from app_analyzer import AnalysisModule  # Assuming your main analysis module is in app_analyzer.py

def analyze_app_lab_analyzer(directory_path):
    # Create an instance of the AnalysisModule
    analysis_module = AnalysisModule(directory_path)
    analysis_module.analyze()

    # Get insights from the AnalysisModule
    app_name = analysis_module.get_name()
    app_creator = analysis_module.get_creator()
    app_purpose = analysis_module.get_purpose()

    # Combine insights
    combined_insights, use_case_insights, comprehensive_report = analysis_module.combine_insights(
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
    app_directory_path = "/home/nick/App_Lab_Analyzer"
    analyze_app_lab_analyzer(app_directory_path)
