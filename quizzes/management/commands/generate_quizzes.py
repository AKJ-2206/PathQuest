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