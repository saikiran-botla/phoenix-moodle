from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Coursescreated,Coursesundertaken, Assignment, Submission, Ta, Announcements, Discussion, chats

class CourseForm(forms.ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Coursescreated
  
        # specify fields to be used
        fields = [
            "title",
            "coursecode",
        ]

class joinCourseForm(forms.ModelForm):
	class Meta:
		model=Coursesundertaken
		fields=["title","joincode",]

class changestatform(forms.ModelForm):
    class Meta:
        model=Coursescreated
        fields=['dis_status']

class createUser(UserCreationForm):
	class Meta:
		model=User
		fields=["username","email","password1","password2"]

class createAssignment(forms.ModelForm):
    class Meta:
        model=Assignment
        fields=["name","file","statement","total","weightage"]

class uploadcsvform(forms.ModelForm):
    class Meta:
        model=Assignment
        fields=['csvfile']

class feedbackform(forms.ModelForm):
    class Meta:
        model=Submission
        fields=['grade',"feedback"]

class submissionform(forms.ModelForm):
    class Meta:
        model=Submission
        fields=['submittedfile']

class addTaform(forms.ModelForm):
    class Meta:
        model=Ta
        fields=["user","enroll_student","givefeedback","create_assignment"]

class modifytaform(forms.ModelForm):
    class Meta:
        model=Ta
        fields=['enroll_student','create_assignment']

class enrollform(forms.ModelForm):
    class Meta:
        model=Coursesundertaken
        fields=['user']

class Announcementform(forms.ModelForm):
    class Meta:
        model=Announcements
        fields=['message']

class discussionform(forms.ModelForm):
    class Meta:
        model=Discussion
        fields=['message']

class chatform(forms.ModelForm):
    class Meta:
        model=chats
        fields=['message']