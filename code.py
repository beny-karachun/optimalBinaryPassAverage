import streamlit as st

def calculate_weighted_average(courses):
    """
    Calculate and return the weighted average.
    courses: list of tuples (grade, credits)
    """
    if not courses:
        return 0.0
    
    total_weighted = 0
    total_credits = 0
    
    for grade, credits in courses:
        total_weighted += grade * credits
        total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    return total_weighted / total_credits

def main():
    st.title("Binary Pass Maximization for Degree Average")

    # ---------------------------------------------------------------
    # STEP 1: PAST COURSES
    # ---------------------------------------------------------------
    st.header("Step 1: Provide Your Past Courses Information")

    # Options for providing past courses:
    #  1) Enter individually
    #  2) Provide overall average & total points
    #  3) Enter past semesters (each with average & total points)
    past_course_option = st.radio(
        "Choose how to provide your past courses:",
        (
            "Enter individually",
            "Provide overall average & total points",
            "Enter each past semester's total points and average (מהיר דרך גליון ציונים)"
        )
    )

    # Will store (grade, credits) for either individual courses, aggregated data, or semester-aggregated data
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
        
        # Convert to (grade, credits) format
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
        # We'll treat this as one "aggregated" record
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
            
            # Accumulate
            total_weighted_sum += sem_avg * sem_credits
            total_credits_sum += sem_credits
        
        # After collecting all semesters, compute overall average
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
        # -----------------------------------------------------------
        # 1) Calculate the average if NO passes are applied
        #    (all courses are counted with their numerical grades)
        # -----------------------------------------------------------
        no_pass_courses_for_average = []
        for course_name, course_credits, course_grade in current_semester_courses:
            no_pass_courses_for_average.append((course_grade, course_credits))
        # Combine past + no-pass new courses
        all_no_pass = past_course_data + no_pass_courses_for_average
        no_pass_average = calculate_weighted_average(all_no_pass)
        
        # -----------------------------------------------------------
        # 2) Identify all passing courses (grade >= 55) from this semester
        # -----------------------------------------------------------
        passing_courses = [
            (n, cr, g) for (n, cr, g) in current_semester_courses if g >= 55
        ]
        
        # -----------------------------------------------------------
        # 3) Sort passing courses by ascending grade
        # -----------------------------------------------------------
        passing_courses_sorted = sorted(passing_courses, key=lambda x: x[2])
        
        # -----------------------------------------------------------
        # 4) Select as many as we are allowed to pass, from the lowest grade up
        # -----------------------------------------------------------
        courses_to_pass = passing_courses_sorted[:binary_passes_available]
        courses_to_pass_names = {c[0] for c in courses_to_pass}
        
        # -----------------------------------------------------------
        # 5) Build a new list of current semester courses for final average calculation
        #    Exclude the "passed" ones from numerical average
        # -----------------------------------------------------------
        included_courses_for_average = []
        for course_name, course_credits, course_grade in current_semester_courses:
            if course_name not in courses_to_pass_names:
                included_courses_for_average.append((course_grade, course_credits))
        
        # Combine with past courses data
        all_courses_for_average = past_course_data + included_courses_for_average
        
        # -----------------------------------------------------------
        # 6) Calculate new average (after pass/fail)
        # -----------------------------------------------------------
        new_average = calculate_weighted_average(all_courses_for_average)
        
        # -----------------------------------------------------------
        # DISPLAY RESULTS
        # -----------------------------------------------------------
        st.subheader("Results")
        st.write(f"**Current Average (Before This Semester)**: {current_average:.2f}")
        st.write(f"**Average Pre-Binary Pass Application**: {no_pass_average:.2f}")
        st.write(f"**New Average (After Optimal Binary Pass Application)**: {new_average:.2f}")
        
        # Show which courses were changed to Pass
        if courses_to_pass_names:
            st.write("**Courses Changed to Pass/Fail (no numerical grade)**:")
            for c in courses_to_pass_names:
                st.write(f"- {c}")
        else:
            st.write("No courses were changed to Pass/Fail.")

if __name__ == "__main__":
    main()
