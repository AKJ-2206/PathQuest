from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Quiz, Question, Answer, UserQuizProgress
import requests

@login_required
def quiz_list(request):
    topics = Topic.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'topics': topics})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = calculate_score(request.POST, quiz)
        UserQuizProgress.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'score': score}
        )
        return render(request, 'quizzes/quiz_result.html', {'quiz': quiz, 'score': score})

def calculate_score(post_data, quiz):
    # Implement score calculation logic here
    pass

# quizzes/views.py
from django.db.models import Q

def search_quizzes(request):
    query = request.GET.get('q')
    if query:
        quizzes = Quiz.objects.filter(
            Q(title__icontains=query) | Q(topic__name__icontains=query)
        )
    else:
        quizzes = Quiz.objects.all()
    return render(request, 'quizzes/search_results.html', {'quizzes': quizzes, 'query': query})



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Quiz, Question

@login_required
def take_quiz(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    quiz = Quiz.objects.filter(topic=topic).first()
    if not quiz:
        # If no quiz exists for this topic, create one
        quiz = Quiz.objects.create(title=f"{topic.name} Quiz", topic=topic)
        generate_questions(quiz)
    
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})

def generate_questions(quiz):
    # This is a placeholder function. In a real application, you'd want to
    # generate questions based on the topic, possibly using an API or a more
    # sophisticated algorithm.
    questions = [
        f"What is a key feature of {quiz.topic.name}?",
        f"Who is considered the founder of {quiz.topic.name}?",
        f"In what year was {quiz.topic.name} first introduced?",
        f"What is a common use case for {quiz.topic.name}?",
        f"Name a popular framework or library used in {quiz.topic.name}."
    ]
    
    for question_text in questions:
        question = Question.objects.create(quiz=quiz, text=question_text)
        Answer.objects.create(question=question, text="Correct Answer", is_correct=True)
        Answer.objects.create(question=question, text="Wrong Answer 1", is_correct=False)
        Answer.objects.create(question=question, text="Wrong Answer 2", is_correct=False)
        Answer.objects.create(question=question, text="Wrong Answer 3", is_correct=False)



# quizzes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Quiz, Question, Answer

@login_required
def take_quiz(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    quiz = Quiz.objects.filter(topic=topic).first()
    if not quiz:
        # If no quiz exists for this topic, create one
        quiz = Quiz.objects.create(title=f"{topic.name} Quiz", topic=topic)
        generate_questions(quiz)
    
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})

def generate_questions(quiz):
    # This is a placeholder function. In a real application, you'd want to
    # generate questions based on the topic, possibly using an API or a more
    # sophisticated algorithm.
    questions = [
        f"What is a key feature of {quiz.topic.name}?",
        f"Who is considered the founder of {quiz.topic.name}?",
        f"In what year was {quiz.topic.name} first introduced?",
        f"What is a common use case for {quiz.topic.name}?",
        f"Name a popular framework or library used in {quiz.topic.name}."
    ]
    
    for question_text in questions:
        question = Question.objects.create(quiz=quiz, text=question_text)
        Answer.objects.create(question=question, text="Correct Answer", is_correct=True)
        Answer.objects.create(question=question, text="Wrong Answer 1", is_correct=False)
        Answer.objects.create(question=question, text="Wrong Answer 2", is_correct=False)
        Answer.objects.create(question=question, text="Wrong Answer 3", is_correct=False)

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = calculate_score(request.POST, quiz)
        UserQuizProgress.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'score': score}
        )
        return render(request, 'quizzes/quiz_result.html', {'quiz': quiz, 'score': score})
    return redirect('quiz_list')

def calculate_score(post_data, quiz):
    score = 0
    questions = Question.objects.filter(quiz=quiz)
    for question in questions:
        if str(question.id) in post_data:
            if question.answer_set.filter(id=post_data[str(question.id)], is_correct=True).exists():
                score += 1
    return score

@login_required
def quiz_list(request):
    topics = Topic.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'topics': topics})