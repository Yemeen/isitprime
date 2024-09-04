import streamlit as st
import random
import time
import math
from database import save_results  

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def main():
    st.set_page_config(layout="centered", page_title="Prime Number Quiz")

    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'home'

    if st.session_state.game_state == 'home':
        st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Welcome to the Prime Number Quiz!</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px;'>An experiment on how humans perceive primes.</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px;'>You'll have 3 seconds to answer each question. Good luck!</p>", unsafe_allow_html=True)
        
        if st.button("Start Quiz", use_container_width=True):
            st.session_state.game_state = 'quiz'
            st.session_state.question_number = 0
            st.session_state.correct_answers = 0
            st.session_state.results = []
            st.rerun()

    elif st.session_state.game_state == 'quiz':
        if st.session_state.question_number < 10:
            if 'start_time' not in st.session_state:
                st.session_state.start_time = time.time()
                st.session_state.number = random.randrange(1, 9999, 2)
                st.session_state.correct_answer = "Prime" if is_prime(st.session_state.number) else "Not Prime"
                st.session_state.answered = False

            st.markdown(f"<h1 style='text-align: center; color: #1E90FF;'>Question {st.session_state.question_number + 1}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; font-size: 48px;'>Is {st.session_state.number} prime?</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                prime_button = st.button("Prime", key="prime", use_container_width=True, 
                                         help="Click if you think the number is prime")
            with col2:
                not_prime_button = st.button("Not Prime", key="not_prime", use_container_width=True,
                                             help="Click if you think the number is not prime")

            timer_placeholder = st.empty()
            progress_bar = st.progress(0)

            current_time = time.time()
            elapsed_time = current_time - st.session_state.start_time
            time_left = max(0, 3.0 - elapsed_time)
            timer_placeholder.metric("Time Remaining", f"{time_left:.1f}s")
            progress_bar.progress(time_left / 3)

            if prime_button or not_prime_button or time_left <= 0:
                st.session_state.answered = True
                user_answer = "Prime" if prime_button else "Not Prime" if not_prime_button else "No answer"
                response_time = min(3.0, elapsed_time)
                
                if user_answer != "No answer":
                    if user_answer == st.session_state.correct_answer:
                        st.session_state.correct_answers += 1
                else:
                    st.warning("Time's up! You didn't answer in time.", icon="⏰")
                
                st.session_state.results.append((st.session_state.number, user_answer, st.session_state.correct_answer, response_time, st.session_state.question_number + 1))
                # Remove the save_result call from here

                st.session_state.question_number += 1
                for key in ['start_time', 'number', 'correct_answer', 'answered']:
                    if key in st.session_state:
                        del st.session_state[key]
                time.sleep(1)
                st.rerun()

            if not st.session_state.answered:
                time.sleep(0.1)
                st.rerun()

        else:
            # Save all results at the end of the quiz
            success, message = save_results(st.session_state.results)
            if success:
                st.success(message)
            else:
                st.error(message)
            st.session_state.game_state = 'results'
            st.rerun()

    elif st.session_state.game_state == 'results':
        st.balloons()  
        st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Quiz Completed!</h1>", unsafe_allow_html=True)
        
        if st.button("Play Again", use_container_width=True):
            st.session_state.game_state = 'home'
            for key in list(st.session_state.keys()):
                if key != 'game_state':
                    del st.session_state[key]
            st.rerun()
        
        correct_count = st.session_state.correct_answers
        incorrect_count = 10 - correct_count
        avg_response_time = sum(result[3] for result in st.session_state.results) / 10

        col1, col2, col3 = st.columns(3)
        col1.metric("Correct Answers", f"{correct_count}/10", f"{correct_count*10}%")
        col2.metric("Incorrect Answers", f"{incorrect_count}/10", f"{incorrect_count*10}%")
        col3.metric("Avg Response Time", f"{avg_response_time:.2f}s")

        st.subheader("Response Times per Question")
        chart_data = {
            "Question": list(range(1, 11)),
            "Response Time": [result[3] for result in st.session_state.results],
            "Correct": [result[1] == result[2] for result in st.session_state.results]
        }
        st.bar_chart(chart_data, x="Question", y="Response Time", color="Correct")

        st.subheader("Detailed Results")
        for i, (number, user_answer, correct_answer, response_time, question_number) in enumerate(st.session_state.results, 1):
            emoji = "✅" if user_answer == correct_answer else "❌"
            color = "#28a745" if user_answer == correct_answer else "#dc3545"
            st.markdown(f"""
            <div style="
                background-color: {color}20;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            ">
                <strong>Q{question_number}:</strong> Number: {number}<br>
                Your answer: {user_answer}<br>
                Correct answer: {correct_answer}<br>
                Time: {response_time:.2f}s {emoji}
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()