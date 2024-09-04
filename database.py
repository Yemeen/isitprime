import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase client setup
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def save_results(results):
    try:
        session_id = supabase.table('quiz_results').insert({
            'question_number': 0,  # Use 0 to mark the session start
            'number': 0,
            'user_answer': '',
            'correct_answer': '',
            'response_time': 0,
            'is_correct': None
        }).execute().data[0]['session_id']

        for number, user_answer, correct_answer, response_time, question_number in results:
            supabase.table('quiz_results').insert({
                'session_id': session_id,
                'question_number': question_number,
                'number': number,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'response_time': response_time,
                'is_correct': user_answer == correct_answer
            }).execute()

        return True, "Quiz results saved successfully!"
    except Exception as e:
        return False, f"An error occurred while saving the results: {str(e)}"