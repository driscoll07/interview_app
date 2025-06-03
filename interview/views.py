from django.shortcuts import render, redirect,get_object_or_404
from .forms import QuestionForm
from .models import Question,Question, InterviewSession, Answer 
import random

from django.core.management import call_command
from django.http import HttpResponse






def home(request):
    return render(request, 'interview/home.html')



def see_questions(request):
    questions = Question.objects.all()
    return render(request, 'interview/see_questions.html', {'questions': questions})

def add_question(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('see_questions')
    return render(request, 'interview/question_form.html', {'form': form})

  


def start_interview(request):
    if request.method == 'POST':
        # Create new interview session
        session = InterviewSession.objects.create()

        # Get 16 random questions
        question_ids = list(Question.objects.values_list('id', flat=True))
        selected_ids = random.sample(question_ids, min(30, len(question_ids)))

        # Store question IDs and session ID in session
        request.session['interview_session_id'] = session.id
        request.session['question_ids'] = selected_ids
        request.session['current_index'] = 0

        return redirect('interview_question')

    return render(request, 'interview/start_interview.html')



def interview_question(request):
    if request.method == 'POST':
        interview_id = request.POST.get('interview_id')
        question_id = request.POST.get('question_id')
        audio_file = request.FILES.get('audio')

        interview = InterviewSession.objects.get(pk=interview_id)
        question = Question.objects.get(pk=question_id)

        Answer.objects.create(
            interview=interview,
            question=question,
            audio=audio_file
        )

        request.session['current_index'] += 1
        return redirect('interview_question')

    question_ids = request.session.get('question_ids')
    current_index = request.session.get('current_index', 0)

    if not question_ids or current_index >= len(question_ids):
        return redirect('interview_result')

    question_id = question_ids[current_index]
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'interview/interview_question.html', {
        'question': question,
        'question_number': current_index + 1,
        'total_questions': len(question_ids),
    })



def interview_result(request):
    session_id = request.session.get('interview_session_id')
    if not session_id:
        return redirect('home')

    interview = get_object_or_404(InterviewSession, pk=session_id)
    answers = Answer.objects.filter(interview=interview).select_related('question')

    # Clean up session
    request.session.pop('interview_session_id', None)
    request.session.pop('question_ids', None)
    request.session.pop('current_index', None)

    return render(request, 'interview/interview_result.html', {
        'interview': interview,
        'answers': answers,
    })




def migrate_db(request):
    call_command("migrate")
    return HttpResponse("Migrations run.")







