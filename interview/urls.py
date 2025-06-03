from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('start/', views.start_interview, name='start_interview'),  # placeholder
    # path('questions/', views.see_questions, name='see_questions'),  # placeholder
    path('questions/add/', views.add_question, name='add_question'),
    path('interview/start/', views.start_interview, name='interview_start'),
    path('interview/question/', views.interview_question, name='interview_question'),
    path('interview/result/', views.interview_result, name='interview_result'),
    path('questions/', views.see_questions, name='see_questions'),

    path('load-data/', views.load_data),

]
