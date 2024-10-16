import os
from django.core.management.base import BaseCommand
from django.conf import settings
from recommender.recommender import CourseRecommender  # Adjust as necessary
from scipy.sparse import hstack  # Add this import

class Command(BaseCommand):
    help = 'Trains the recommendation model'

    def add_arguments(self, parser):
        parser.add_argument('Course_info1', type=str, help='/Volumes/Coding2/tri4e/Project/prototype3/PathQuest/recommender/Course_info1.csv')

    def handle(self, *args, **options):
        dataset_name = options['Course_info1']
        dataset_path = os.path.join(settings.BASE_DIR, 'data', dataset_name)

        # Debugging: print the dataset path to verify it's correct
        print(f"Dataset path: {dataset_path}")
        
        if not os.path.exists(dataset_path):
            self.stderr.write(self.style.ERROR(f'Dataset file not found: {dataset_path}'))
            return

        try:
            recommender = CourseRecommender()  # Instantiate the recommender
            recommender.train_model(dataset_path)  # Train the model with the dataset
            self.stdout.write(self.style.SUCCESS('Successfully trained model'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error training model: {str(e)}'))
