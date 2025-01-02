import streamlit as st
from itertools import combinations

def calculate_weighted_average(courses):
    """
    Calculate and return the weighted average.
    'courses' should be a list of (grade, credits).
    If no courses or total_credits = 0, returns 0.0
    """
    if not courses:
        return 0.0
    
    total_weighted = 0.0
    total_credits = 0.0
    
    for grade, credits in courses:
        total_weighted += grade * credits
        total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    return total_weighted / total_credits


def compute_average_with_pass_subset(past_courses, current_sem_courses, pass_subset):
    """
    Given:
      - past_courses: list of (grade, credits) for *past* courses
      - current_sem_courses: list of (course_name, course_credits, course_grade)
      - pass_subset: set of course names to treat as Pass (excluded from average)
    
    Return the resulting degree average.
    """
    # Convert current-sem courses to (grade, credits) *excluding* those in pass_subset
    included_for_avg = []
    for c_name, c_credits, c_grade in current_sem_courses:
        if c_name not in pass_subset:
            included_for_avg.append((c_grade, c_credits))
    
    # Combine with past courses
    all_for_avg = past_courses + included_for_avg
    
    return calculate_weighted_average(all_for_avg)


def main():
    st.title("Binary Pass Maximization for Degree Average (Optimal Subset)")

    # ---------------------------------------------------------------
    # STEP 1: PAST COURSES
    # ---------------------------------------------------------------
    st.header("Step 1: Provide Your Past Courses Information")

    past_course_option = st.radio(
        "Choose how to provide your past courses:",
        (
            "Enter individually",
            "Provide overall average & total points",
            "Enter past semesters (averages & points)"
        )
    )

    # Will store (grade, credits) from whichever method the user chooses
    past_course_data = []
    
    # ---------------------------------------------------------------
    # 1) ENTER INDIVIDUALLY
    # ---------------------------------------------------------------
    if past_course_option == "Enter individually":
        num_past_courses = st.number_input(
            "How many past courses have you completed?",
            min_value=0, step=1
        )
        
        past_courses = []
        for i in range(num_past_courses):
            st.subheader(f"Past Course #{i+1}")
            col1, col2, col3 = st.columns(3)
            with col1:
                course_name = st.text_input(
                    f"Name of course #{i+1}:",
                    key=f"past_name_{i}"
                )
            with col2:
                course_credits = st.number_input(
                    f"Credits for {course_name}:",
                    min_value=0.0, step=0.5, key=f"past_credits_{i}"
                )
            with col3:
                course_grade = st.number_input(
                    f"Grade for {course_name} (0-100):",
                    min_value=0, max_value=100, step=1, key=f"past_grade_{i}"
                )
            past_courses.append((course_name, course_credits, course_grade))
        
        # Convert to (grade, credits) for average calculation
        past_course_data = [(c[2], c[1]) for c in past_courses]  # (grade, credits)

    # ---------------------------------------------------------------
    # 2) PROVIDE OVERALL AVERAGE & TOTAL POINTS
    # ---------------------------------------------------------------
    elif past_course_option == "Provide overall average & total points":
        st.subheader("Enter your aggregated Past Courses information")
        overall_past_average = st.number_input(
            "Overall average for your past courses (0-100):",
            min_value=0.0, max_value=100.0, step=0.1
        )
        total_past_credits = st.number_input(
            "Total credit points accumulated so far:",
            min_value=0.0, step=0.5
        )
        if total_past_credits > 0:
            past_course_data = [(overall_past_average, total_past_credits)]
        else:
            past_course_data = []

    # ---------------------------------------------------------------
    # 3) ENTER PAST SEMESTERS (AVERAGES & POINTS)
    # ---------------------------------------------------------------
    else:  # "Enter past semesters (averages & points)"
        st.subheader("Provide each semester's average and credit points")
        
        num_past_semesters = st.number_input(
            "How many past semesters do you have?",
            min_value=0, step=1
        )
        
        total_weighted_sum = 0.0
        total_credits_sum = 0.0
        
        for i in range(num_past_semesters):
            st.subheader(f"Semester #{i+1}")
            col1, col2 = st.columns(2)
            with col1:
                sem_avg = st.number_input(
                    f"Semester #{i+1} Average (0-100):",
                    min_value=0.0, max_value=100.0, step=0.1, key=f"sem_avg_{i}"
                )
            with col2:
                sem_credits = st.number_input(
                    f"Semester #{i+1} Total Credits:",
                    min_value=0.0, step=0.5, key=f"sem_credits_{i}"
                )
            
            total_weighted_sum += sem_avg * sem_credits
            total_credits_sum += sem_credits
        
        if total_credits_sum > 0:
            overall_average = total_weighted_sum / total_credits_sum
            past_course_data = [(overall_average, total_credits_sum)]
        else:
            past_course_data = []

    # ---------------------------------------------------------------
    # Compute Current Average (before this semester)
    # ---------------------------------------------------------------
    current_average = calculate_weighted_average(past_course_data)
    st.write("---")
    st.write(f"**Current Degree Average (Before This Semester)**: {current_average:.2f}")
    st.write("---")

    # ---------------------------------------------------------------
    # STEP 2: BINARY PASS INFORMATION
    # ---------------------------------------------------------------
    st.header("Step 2: Binary Pass Information")
    binary_passes_available = st.number_input(
        "How many Binary Passes (Pass/Fail) can you apply this semester?",
        min_value=0, step=1
    )

    # ---------------------------------------------------------------
    # STEP 3: ENTER THIS SEMESTER'S COURSES
    # ---------------------------------------------------------------
    st.header("Step 3: Enter This Semester's Courses")
    num_current_sem_courses = st.number_input(
        "How many courses are you taking this semester?",
        min_value=0, step=1
    )
    
    current_semester_courses = []
    for i in range(num_current_sem_courses):
        st.subheader(f"This Semester Course #{i+1}")
        col1, col2, col3 = st.columns(3)
        with col1:
            course_name = st.text_input(
                f"Name of course #{i+1}:",
                key=f"current_name_{i}"
            )
        with col2:
            course_credits = st.number_input(
                f"Credits for {course_name}:",
                min_value=0.0, step=0.5, key=f"current_credits_{i}"
            )
        with col3:
            course_grade = st.number_input(
                f"Grade for {course_name} (0-100):",
                min_value=0, max_value=100, step=1, key=f"current_grade_{i}"
            )
        current_semester_courses.append((course_name, course_credits, course_grade))

    # ---------------------------------------------------------------
    # BUTTON TO PERFORM CALCULATION
    # ---------------------------------------------------------------
    if st.button("Calculate Optimal Pass/Fail"):
        # 1) Average if NO passes are applied
        no_pass_list = [
            (c_grade, c_credits) for (c_name, c_credits, c_grade) in current_semester_courses
        ]
        all_no_pass = past_course_data + no_pass_list
        pre_pass_average = calculate_weighted_average(all_no_pass)

        # 2) Identify passing courses (grade >= 55)
        passing_courses = [(n, cr, g) for (n, cr, g) in current_semester_courses if g >= 55]
        passing_course_names = [pc[0] for pc in passing_courses]
        pass_limit = min(len(passing_courses), binary_passes_available)

        # 3) Try all subsets of the passing courses up to pass_limit
        #    We'll keep track of the best average and subset
        best_average = -1.0
        best_subset = set()

        # We'll pass from 0 up to pass_limit courses
        for r in range(pass_limit + 1):
            for combo in combinations(passing_course_names, r):
                pass_subset = set(combo)
                # Compute average if we pass these 'r' courses
                candidate_avg = compute_average_with_pass_subset(
                    past_courses=past_course_data,
                    current_sem_courses=current_semester_courses,
                    pass_subset=pass_subset
                )
                if candidate_avg > best_average:
                    best_average = candidate_avg
                    best_subset = pass_subset

        # 4) Display results
        st.subheader("Results")
        st.write(f"**Current Average (Before This Semester)**: {current_average:.2f}")
        st.write(f"**Average Pre-Binary Pass Application (All Graded This Semester)**: {pre_pass_average:.2f}")
        st.write(f"**New Average (After Optimal Binary Pass Application)**: {best_average:.2f}")

        if best_subset:
            st.write("**Courses Changed to Pass/Fail (no numerical grade):**")
            for c in best_subset:
                st.write(f"- {c}")
        else:
            st.write("No courses were changed to Pass/Fail.")


if __name__ == "__main__":
    main()
