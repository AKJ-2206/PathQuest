# quizzes/api.py
import requests
from django.core.exceptions import ImproperlyConfigured
from .models import Quiz, Question, Answer, Topic
import random

def generate_quiz(topic):
    try:
        # Replace with actual API endpoint and key
        api_url = "https://api.example.com/generate_quiz"
        api_key = "your_api_key_here"
        
        params = {
            "topic": topic,
            "num_questions": 10
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            quiz_data = response.json()
            # Process and save the quiz data to your database
            save_quiz_to_database(quiz_data)
        else:
            # Handle API error
            raise ImproperlyConfigured("API request failed")
    except (requests.RequestException, ImproperlyConfigured):
        # Fallback to generating a simple quiz without API
        generate_simple_quiz(topic)

def generate_simple_quiz(topic):
    # Create a new quiz
    topic_obj, _ = Topic.objects.get_or_create(name=topic)
    quiz = Quiz.objects.create(title=f"{topic.capitalize()} Quiz", topic=topic_obj)

    # Generate simple questions
    questions = [
        f"What is a key feature of {topic}?",
        f"Who is considered the founder of {topic}?",
        f"In what year was {topic} first introduced?",
        f"What is a common use case for {topic}?",
        f"Name a popular framework or library used in {topic}."
    ]

    for question_text in questions:
        question = Question.objects.create(quiz=quiz, text=question_text)
        
        # Generate dummy answers
        Answer.objects.create(question=question, text="Answer 1", is_correct=True)
        Answer.objects.create(question=question, text="Answer 2", is_correct=False)
        Answer.objects.create(question=question, text="Answer 3", is_correct=False)
        Answer.objects.create(question=question, text="Answer 4", is_correct=False)

    print(f"Generated a simple quiz for {topic}")

def save_quiz_to_database(quiz_data):
    # Implement logic to save the quiz data to your database
    pass

# quizzes/management/commands/generate_quizzes.py
from django.core.management.base import BaseCommand
from quizzes.api import generate_quiz

class Command(BaseCommand):
    help = 'Generates quizzes for a given topic'

    def add_arguments(self, parser):
        parser.add_argument('topic', type=str)

    def handle(self, *args, **options):
        topic = options['topic']
        generate_quiz(topic)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated quiz for {topic}'))