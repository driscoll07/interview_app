from django.db import models

class Question(models.Model):
    text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text[:50]

class InterviewSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Answer(models.Model):
    interview = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='answers/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to Q{self.question.id} in Session {self.interview.id}"
