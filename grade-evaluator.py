import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    # Handle an empty CSV gracefully
    if not data:
        print("Error: No assignment records found in the file. Nothing to evaluate.")
        return

    # a) Check if all scores are percentage based (0-100)
    for item in data:
        if not (0 <= item['score'] <= 100):
            print(f"Error: '{item['assignment']}' has an invalid score of {item['score']}. "
                  f"Scores must be between 0 and 100.")
            sys.exit(1)

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    total_weight = sum(item['weight'] for item in data)
    formative_weight = sum(item['weight'] for item in data if item['group'].lower() == 'formative')
    summative_weight = sum(item['weight'] for item in data if item['group'].lower() == 'summative')

    if total_weight != 100:
        print(f"Error: Total weight is {total_weight}, but it must equal 100.")
        sys.exit(1)
    if formative_weight != 60:
        print(f"Error: Formative weight is {formative_weight}, but it must equal 60.")
        sys.exit(1)
    if summative_weight != 40:
        print(f"Error: Summative weight is {summative_weight}, but it must equal 40.")
        sys.exit(1)

    # c) Calculate the Final Grade and GPA
    formative_total = sum(
        (item['score'] * item['weight'] / 100) for item in data if item['group'].lower() == 'formative'
    )
    summative_total = sum(
        (item['score'] * item['weight'] / 100) for item in data if item['group'].lower() == 'summative'
    )
    final_grade = formative_total + summative_total
    gpa = (final_grade / 100) * 5.0

    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_pass = formative_total >= 30   # 50% of 60
    summative_pass = summative_total >= 20   # 50% of 40
    passed = formative_pass and summative_pass
    status = "PASSED" if passed else "FAILED"

    # e) Check for failed formative assignments (< 50%) and determine
    #    which one(s) have the highest weight for resubmission.
    failed_formatives = [
        item for item in data
        if item['group'].lower() == 'formative' and item['score'] < 50
    ]

    if failed_formatives:
        max_weight = max(item['weight'] for item in failed_formatives)
        resubmission_candidates = [
            item['assignment'] for item in failed_formatives if item['weight'] == max_weight
        ]
        resubmission_text = ", ".join(resubmission_candidates)
    else:
        resubmission_text = "None"

    # f) Print the final decision as a formatted transcript table
    col_assignment, col_category, col_grade, col_weight, col_final = 38, 10, 10, 8, 12

    print()
    print(f"{'Assignment':<{col_assignment}}{'Category':<{col_category}}"
          f"{'Grade (%)':<{col_grade}}{'Weight':<{col_weight}}{'Final weight':<{col_final}}")
    print("-" * (col_assignment + col_category + col_grade + col_weight + col_final))

    for item in data:
        category_code = "FA" if item['group'].lower() == 'formative' else "SA"
        final_weight = item['score'] * item['weight'] / 100
        print(f"{item['assignment']:<{col_assignment}}{category_code:<{col_category}}"
              f"{item['score']:<{col_grade}.0f}{item['weight']:<{col_weight}.0f}{final_weight:<{col_final}.2f}")

    print("-" * (col_assignment + col_category + col_grade + col_weight + col_final))
    print(f"{'Formatives (60)':<{col_assignment + col_category + col_grade + col_weight}}{formative_total:.2f}")
    print(f"{'Summatives (40)':<{col_assignment + col_category + col_grade + col_weight}}{summative_total:.2f}")
    print(f"{'GPA':<{col_assignment + col_category + col_grade + col_weight}}{gpa:.3f}")
    print(f"{'Status':<{col_assignment + col_category + col_grade + col_weight}}{status}")
    print(f"{'Available for resubmission':<{col_assignment + col_category + col_grade + col_weight}}{resubmission_text}")
    print()


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
