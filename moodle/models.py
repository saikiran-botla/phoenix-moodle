from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Coursescreated(models.Model):
  	user = models.ForeignKey(User, on_delete = models.CASCADE)
  	title = models.CharField(max_length = 50)
  	coursecode = models.CharField(max_length=5,validators=[RegexValidator(regex=r'^\w{5}$', message='Length has to be 5')])
  	dis_status=models.BooleanField(default=True)

  	def __str__(self):
  		return self.title



class Coursesundertaken(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title=models.CharField(max_length=50)
	joincode=models.CharField(max_length=5)
	def __str__(self):
		return self.title


class Assignment(models.Model):
  	course = models.ForeignKey(Coursescreated, on_delete = models.CASCADE)
  	name = models.CharField(max_length = 50)
  	file=models.FileField(upload_to='',blank=True)
  	statement = models.TextField(blank=True)
  	total = models.PositiveIntegerField()
  	date_created=models.DateTimeField(auto_now_add=True,null=True)
  	deadline=models.DateTimeField(null = True,blank=True)
  	csvfile = models.FileField(upload_to='',blank=True)
  	weightage=models.DecimalField(max_digits=5,decimal_places=2,null=True)
  	#histogram=models.ImageField(upload_to='',blank=True,null=True)

  	def __str__(self):
  		return self.name
  
class Submission(models.Model):
  	assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
  	student = models.ForeignKey(User, on_delete=models.CASCADE)
  	submittedfile = models.FileField(upload_to='',blank=True)
  	grade = models.PositiveIntegerField(null = True, blank=True)
  	statusofcorrection = models.CharField(max_length=100,default = "NOT DONE")
  	feedback = models.TextField(null = True, blank=True)
  	
  	def __str__(self):
  		return self.student.username


class Ta(models.Model):
	
	course=models.ForeignKey(Coursescreated, on_delete = models.CASCADE)
	user=models.ForeignKey(User, on_delete = models.CASCADE)
	enroll_student=models.BooleanField(default=False)
	givefeedback=models.BooleanField(default=True)
	create_assignment=models.BooleanField(default=False)
	
	def __str__(self):
 		return self.user.username

class Announcements(models.Model):
	course=models.ForeignKey(Coursescreated, on_delete = models.CASCADE)
	message=models.TextField(null = True)

	def __str__(self):
		return self.course.title


class Discussion(models.Model):
	course=models.ForeignKey(Coursescreated,on_delete = models.CASCADE)
	message=models.TextField(null = True)
	user=models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.course.title

class chats(models.Model):
	sender=models.ForeignKey(User,null=True,related_name='sender',on_delete = models.CASCADE)
	receiver = models.ForeignKey(User,null = True, related_name='receiver',on_delete = models.CASCADE)
	message=models.TextField(null=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return self.sender.username