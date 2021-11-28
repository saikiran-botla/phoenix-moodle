from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.images import ImageFile
from django.core.mail import send_mail


from .forms import createUser,CourseForm,joinCourseForm, createAssignment,feedbackform, submissionform, uploadcsvform,changestatform, addTaform, enrollform, modifytaform, Announcementform, discussionform, chatform
from .models import Coursescreated, Assignment, Submission, Coursesundertaken, Ta, Announcements, Discussion, chats

import datetime
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import urllib, base64
from random import randint


def loginPage(request):

	if request.user.is_authenticated:
		return redirect('home')

	context={}

	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(request,username=username,password=password)
		#return HttpResponse(user)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,"username or password is incorrect")
			#return render(request,'./moodle/login.html',context)

	return render(request,'./moodle/login.html',context)

def signup(request):

	if request.user.is_authenticated:
		return redirect('home')

	form=createUser()

	if request.method=="POST":
		form=createUser(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,"Account was created for "+form.cleaned_data.get("username"))
			return redirect('login')

	context={'form':form}
	return render(request,'./moodle/signup.html',context)

@login_required(login_url='login')
def logoutPage(request):
	logout(request)
	return redirect('login')

OTP=randint(100000,999999)
@login_required(login_url='login')
def reset(request):

	#OTP=randint(100000,999999)
	send_mail(
		"OTP for password change",
		"Here is your OTP for password change :"+str(OTP)+".\n please enter carefully without anyspaces before or between or after the digits",
		'1457205saikiran@gmail.com',
		[request.user.email],
		fail_silently=True,
		)

	if request.method=="POST":

		OTPgi=request.POST.get('OTP')
		if OTP != int(OTPgi):
			form=PasswordChangeForm(request.user)
			messages.error(request,"OTP is incorrect"+str(OTPgi) + str(OTP))
			return render(request,'./moodle/reset.html',{'form':form}) 

		form=PasswordChangeForm(request.user,request.POST)
		if form.is_valid():
			user=form.save()
			update_session_auth_hash(request,user)
			messages.success(request,"Your password was is successfully updated")
			logout(request)
			return redirect('login')
		else:
			messages.error(request,"Error in Old password or Conformation of password")
			return render(request,'./moodle/reset.html',{'form':form})

	else:

		form=PasswordChangeForm(request.user)
		return render(request,'./moodle/reset.html',{'form':form})



@login_required(login_url='login')
def createcourse(request):

	context={}

	if request.method=="POST":
		form=CourseForm(request.POST)
		if form.is_valid():
			username=request.user
			title=request.POST.get('title')
			check=Coursescreated.objects.all()
			titlecheck=list()
			for e in check:
				titlecheck.append(e.title)
			if title in titlecheck:
				return HttpResponse("Title already exists")
			
			coursecode=request.POST.get('coursecode')
			if len(coursecode)<5:
				return HttpResponse('Coursecode not valid')
			course=Coursescreated(user=username,title=title,coursecode=coursecode)
			course.save()
			send_mail(
				'Your course ' + title +' is successfully created',
				'This is the confirmation mail for successfully creating the course '+title+' in the moodle plaform, you can do a tone of things in the course like create assignment, enroll students for the course , add Ta, make Announcements and more, You can invite user to take your course or join them with the coursecode '+coursecode,
				'1457205saikiran@gmail.com',
				[request.user.email],
				fail_silently=True,

				)
			return redirect('home')




	form=CourseForm()
	context['form']=form
	return render(request,'moodle/createcourse.html',context)


@login_required(login_url='login')
def joincourse(request):
	context={}

	if request.method=="POST":
		form=joinCourseForm(request.POST)
		if form.is_valid():
			title1=request.POST.get('title')
			joincode=request.POST.get('joincode')
			a=Coursescreated.objects.get(title=title1)
			username=request.user
			if username==a.user:
				return HttpResponse("You cant join beacuse you are the instructor for this course")
			if joincode==a.coursecode:
				joined=Coursesundertaken(user=request.user,title=title1,joincode=a.coursecode)
				joined.save()
				return redirect('home')



	form=joinCourseForm()
	context['form']=form

	return render(request,'moodle/joincourse.html',context)


@login_required(login_url='login')
def home(request):
	
    context={}
    return render(request,'./moodle/home.html')

@login_required(login_url='login')
def yourcourse(request):
	courses=Coursescreated.objects.filter(user=request.user)

	todo=list()


	for course in courses:
		assignments=Assignment.objects.filter(course=course)
		for assignment in assignments:
			#eva=True
			submissions=Submission.objects.filter(assignment=assignment)
			for submission in submissions:
				if submission.statusofcorrection=="NOT DONE":
					todo.append(assignment)
					break




	return render(request,'moodle/yourcourse.html',{'courses':courses,'todo':todo})

@login_required(login_url='login')
def joinedcourse(request):
	courses=Coursesundertaken.objects.filter(user=request.user)

	todo=list()

	today=datetime.datetime.now()

	for course in courses:
		cour=Coursescreated.objects.filter(title=course.title)
		assignments=Assignment.objects.filter(course=cour[0])
		for assignment in assignments:
			#sub=Submission.objects.filter(assignment=assignment,student=request.user)
			if Submission.objects.filter(assignment=assignment,student=request.user).exists() :
				continue
			else:
				todo.append(assignment)

	return render(request,'moodle/joinedcourse.html',{'courses':courses,'todo':todo,'today':today})

@login_required(login_url='login')
def instructor(request,pk):
	form=changestatform()
	title=pk
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	Assignments=Assignment.objects.filter(course=course)
	
	mean=list()
	var=list()
	for assignment in Assignments:
		x=list()
		submissions=Submission.objects.filter(assignment=assignment)
		for submission in submissions:
			if submission.statusofcorrection=="DONE":
				x.append(submission.grade)

		x=np.array(x)
		mean.append(np.mean(x))
		var.append(np.var(x))

	total=np.size(mean)
	x=np.arange(1,total+1)

	plt.title('Statistics of course as of now')
	plt.xlabel('Assignment number')
	plt.ylabel('mean and variance')
	plt.plot(x,mean,label='mean')
	plt.plot(x,var,label='variance')
	plt.legend()
	
	buf=io.BytesIO()
	plt.savefig(buf,format='png',dpi=300)
	image_base64=base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n','')
	buf.close()
	plt.clf()
	if request.method == 'POST':
		cou=Coursescreated.objects.get(title=pk)
		stat=request.POST.get('dis_status')
		if stat == 'on' :
			cou.dis_status=True
		else:
			cou.dis_status=False
		cou.save()
		return render(request,'moodle/instructor.html',{'Assignments':Assignments,'title':title,'form':form,'course':cou,'image_base64':image_base64})


	return render(request,'moodle/instructor.html',{'Assignments':Assignments,'title':title,'form':form,'course':course,'image_base64':image_base64})

@login_required(login_url='login')
def student(request,pk):
	course=Coursesundertaken.objects.filter(title=pk)
	course=Coursescreated.objects.filter(title=course[0])
	Assignments=Assignment.objects.filter(course=course[0])

	total=0
	com=0
	for assignment in Assignments:
		if Submission.objects.filter(assignment=assignment,student=request.user).exists() :
			com+=1
		total+=1

	com=(com*100.0)/total
	return render(request,'moodle/student.html',{'Assignments':Assignments,'pk':pk,'course':course[0],'com':com})


@login_required(login_url='login')
def createAss(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]

	context={}

	if request.method=="POST":

		name1=request.POST.get('name')
		file=request.FILES.get('file')
		statement=request.POST.get('statement')
		total=request.POST.get('total')
		deadline=request.POST.get('Due date')
		weightage=request.POST.get('weightage')
		titlecheck=Assignment.objects.filter(course=course)
		check=list()
		for a in titlecheck:
			check.append(a.name)
		if name1 in check:
			return render(request,'moodle/Assignment.html',{'form':createAssignment(),'mes':'This title for assignment already exists please try using another name','course':course})
		Ass=Assignment(course=course,name=name1,file=file,statement=statement,total=total,deadline=deadline,weightage=weightage)
		Ass.save()

		cous=Coursesundertaken.objects.filter(title=pk)
		emails=list()
		for cou in cous:
			emails.append(cou.user.email)

		send_mail(
			'New Assignment '+ name1 +' is relased in the course '+ pk,
			'Your instructor created a new assignment '+ name1 +' in the course '+pk+'\n Please check the course page for further details. \n Due date is '+deadline+'.',
			'1457205saikiran@gmail.com',
			emails,
			)

		return redirect('instructor',pk)
	
	form=createAssignment()
	context['form']=form
	context['course']=course
	return render(request,'moodle/Assignment.html',context)


@login_required(login_url='login')
def viewSubmission(request,pk,ak):
	form=uploadcsvform()
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	assignment=Assignment.objects.filter(course=course,name=ak)
	assignment=assignment[0]
	submissions=Submission.objects.filter(assignment=assignment)

	x=list()
	for submission in submissions:
		if submission.statusofcorrection=='DONE':
			x.append(submission.grade)

	x=np.array(x)
	mean=np.mean(x)
	var=np.var(x)

	plt.title('Histogram of Student marks')
	plt.xlabel('Marks')
	plt.hist(x)

	buf=io.BytesIO()
	plt.savefig(buf,format='png',dpi=300)
	image_base64=base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n','')
	buf.close()
	plt.clf()
	
	if request.method == 'POST':
		form1=uploadcsvform(request.POST)
		if form1.is_valid():
			file=request.FILES.get('csvfile')
				
			name=''
			for line in file:
				line=line.strip()
				line=line.split()
				name=line[0]
				name=name.decode('utf-8')
				
				stu=User.objects.get(username=name)

				if Submission.objects.filter(assignment=assignment,student=stu).exists():
					sub=Submission.objects.get(assignment=assignment,student=stu)
					sub.statusofcorrection="DONE"
					sub.grade=line[1].decode('utf-8')
					feedback=''
					for word in line[2:]:
						feedback+=word.decode('utf-8')+' '
					sub.feedback=feedback
					sub.save()
				send_mail(
					'Your grades are for assignment '+ assignment.name+' of the course '+course.title,
					'Your grades are up for the assignment '+assignment.name+ '. \n Please note that your grade is subject to change from cribs',
					'1457205saikiran@gmail.com',
					[stu.email],
					)
			
			assignment.csvfile=file
			assignment.save()
			return render(request,'moodle/viewsubmissions.html',{'submissions':submissions,'pk':course.title,'ak':assignment.name,'assignment':assignment,'form':form,'mean':mean,'var':var,'image_base64':image_base64})			

		else:
			return render(request,'moodle/viewsubmissions.html',{'submissions':submissions,'pk':course.title,'ak':assignment.name,'assignment':assignment,'form':form,'mean':mean,'var':var,'image_base64':image_base64})						 


	return render(request,'moodle/viewsubmissions.html',{'submissions':submissions,'pk':course.title,'ak':assignment.name,'assignment':assignment,'form':form,'mean':mean,'var':var,'image_base64':image_base64})


@login_required(login_url='login')
def grade(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	assignments=Assignment.objects.filter(course=course)
	
	mysubmissions=list()

	coursetotal=0

	mean=dict()
	y=list()

	for assignment in assignments:
		
		x=list()
		subss=Submission.objects.filter(assignment=assignment)

		for subs in subss:
			if subs.statusofcorrection=="DONE":
				x.append(subs.grade)
		x=np.array(x)
		mean['assignment']=np.mean(x)


		if Submission.objects.filter(assignment=assignment,student=request.user).exists():
			sub=Submission.objects.get(student=request.user,assignment=assignment)
			if sub.statusofcorrection=="DONE" :
				coursetotal=float(assignment.weightage)/100.0 * (int(sub.grade) * 100.0)/assignment.total
				y.append(sub.grade*100.0/assignment.total)
			mysubmissions.append(sub)

	

	y=np.array(y)

	z=np.arange(1,np.size(y)+1)
	plt.plot(z,y)
	plt.xlabel("Assignment number")
	plt.ylabel("percentage of marks obtained")
	plt.title("Your progress")

	buf=io.BytesIO()
	plt.savefig(buf,format='png',dpi=300)
	image_base64=base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n','')
	buf.close()
	plt.clf()

	return render(request,'moodle/grades.html',{'assignments':assignments,'mysubmissions':mysubmissions,'pk':pk,'coursetotal':coursetotal,'mean':mean,'image_base64':image_base64})

	

@login_required(login_url='login')
def feedform(request,pk,ak,sk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	assignment=Assignment.objects.filter(course=course,name=ak)
	assignment=assignment[0]
	student=User.objects.filter(username=sk)
	student=student[0]
	a=Submission.objects.get(assignment=assignment,student=student)

	if request.method=="POST":
		grade=request.POST.get('grade')
		feedback=request.POST.get('feedback')
		a.grade=grade
		a.feedback=feedback
		a.statusofcorrection="DONE"
		a.save()
		send_mail(
			'Your grades are for assignment '+ assignment.name+' of the course '+course.title,
			'Your grades are up for the assignment '+assignment.name +'. \n Please note that your grade is subject to change from cribs',
			'1457205saikiran@gmail.com',
			[student.email],
			)
		#redirectpath='http://127.0.0.1:8000/viewsubmissions/'+pk+'/'+ak+'/'
		return redirect('viewsubmissions',pk,ak)

	form=feedbackform()
	return render(request,'moodle/feedbackform.html',{'form':form})
	


@login_required(login_url='login')
def viewassignment(request,pk,ak):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	assignment=Assignment.objects.filter(course=course,name=ak)
	assignment=assignment[0]
	submissions=Submission.objects.filter(assignment=assignment)

	today=datetime.datetime.now()

	submitted=False
	for submission in submissions:
		if submission.student.username ==request.user.username:
			submitted=True
			mysubmission=submission

	if submitted:
		form=submissionform()
		if request.method=='POST':
			file=request.FILES.get('submittedfile')
			mysubmission.submittedfile=file
			mysubmission.save()
			send_mail(
				"You have submitted your assignment submission for "+ assignment.name +" ",
				"You have submitted your submission for "+ assignment.name +" ",
				'1457205saikiran@gmail.com',
				[request.user.email]
				)
			return render(request,'moodle/viewassignmentyes.html',{'assignment':assignment,'mysubmission':mysubmission,'pk':pk,'form':form,'today':today})

		return render(request,'moodle/viewassignmentyes.html',{'assignment':assignment,'mysubmission':mysubmission,'pk':pk,'form':form,'today':today})
	else:
		form=submissionform()
		if request.method=="POST":
			file=request.FILES.get('submittedfile')
			sub=Submission(assignment=assignment,student=request.user,submittedfile=file)
			sub.save()
			send_mail(
				"You have submitted your assignment submission for "+ assignment.name +" ",
				"You have submitted your submission for "+ assignment.name +" ",
				'1457205saikiran@gmail.com',
				[request.user.email]
				)
			return render(request,'moodle/viewassignmentyes.html',{'assignment':assignment,'mysubmission':sub,'pk':pk,'form':form,'today':today})

		form=submissionform()
		return render(request,'moodle/viewassignmentno.html',{'assignment':assignment,'form':form,'pk':pk,'today':today})

@login_required(login_url='login')
def addTa(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]

	if request.method=="POST":
		username=request.POST['user']
		user=User.objects.get(id=username)
		enroll_student=request.POST.get('enroll_student')
		if enroll_student=='on':
			enroll_student=True
		else:
			enroll_student=False
		givefeedback=request.POST.get('givefeed')
		if givefeedback=='on':
			givefeedback=True
		else:
			givefeedback=False
		create_ass=request.POST.get('create_assignment',False)
		if create_ass=='on':
			create_ass=True
		else:
			create_ass=False
		student=Coursesundertaken.objects.filter(title=pk)
		students=list()
		for a in student:
			students.append(a.user)
		if user in students:
			form=addTaform()
			return render(request,'moodle/addTa.html',{'form':form,'pk':pk,'mes':'This user is a student for this course please select another ta'})
		
		if user==request.user:
			form=addTaform()
			return render(request,'moodle/addTa.html',{'form':form,'pk':pk,'mes':'your are the instructor for this course'})

		t=Ta(course=course,user=user,enroll_student=enroll_student,givefeedback=givefeedback,create_assignment=create_ass)
		t.save()
		return redirect('instructor',pk)

	form=addTaform()
	return render(request,'moodle/addTa.html',{'form':form,'pk':pk})


@login_required(login_url='login')
def enroll(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	form=enrollform()
	if request.method=='POST':
		userid=request.POST['user']
		user=User.objects.get(id=userid)
		if user==course.user:
			form=enrollform()
			return render(request,'moodle/enroll.html',{'form':form,'mes':'This user is instructor for this course','pk':pk})
		ta=Ta.objects.filter(course=course)
		for a in ta:
			if user==a.user:
				form=enrollform()
				return render(request,'moodle/enroll.html',{'form':form,'mes':'This user is a ta for this course','pk':pk})

		students=Coursesundertaken.objects.filter(title=pk)
		for a in students:
			if user==a.user:
				form=enrollform()
				return render(request,'moodle/enroll.html',{'form':form,'mes':'This user is already enrolled in this course','pk':pk})

		#enroll=Coursesundertaken(user=user,title=pk,joincode=course.coursecode)
		send_mail(
			'Invitation for course '+pk,
			'The User '+course.user.username+' invites you for taking the course '+pk+'. Join using this code : '+course.coursecode+'.',
			'1457205saikiran@gmail.com',
			[user.email],
			fail_silently=True,

			)
		return render(request,'moodle/enroll.html',{'form':form,'mes':'Invitation mail is sent successfully','pk':pk})

	return render(request,'moodle/enroll.html',{'form':form,'pk':pk})



@login_required(login_url='login')
def tacourses(request):
	objs=Ta.objects.filter(user=request.user)
	courses=list()
	for a in objs:
		courses.append(a.course)
	return render(request,'moodle/viewta.html',{'courses':courses})


@login_required(login_url='login')
def viewtacourses(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	obj=Ta.objects.filter(user=request.user,course=course)
	obj=obj[0]
	givefeedback=obj.givefeedback
	enroll_student=obj.enroll_student
	create_assignment=obj.create_assignment

	Assignments=Assignment.objects.filter(course=course)
	return render(request,'moodle/viewtacourses.html',{'Assignments':Assignments,'title':pk,'givefeedback':givefeedback,'enroll_student':enroll_student,'create_assignment':create_assignment})


@login_required(login_url='login')
def viewta(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	tas=Ta.objects.filter(course=course)

	users=list()

	for a in tas:
		users.append(a.user)

	return render(request,'moodle/viewtas.html',{'users':users,'pk':pk})


@login_required(login_url='login')
def modifyta(request,pk,ak):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	user=User.objects.filter(username=ak)
	user=user[0]
	ta=Ta.objects.get(course=course,user=user)

	if request.method == 'POST':
		form=modifytaform(request.POST)
		if form.is_valid():
			enroll_student=request.POST.get('enroll_student')
			if enroll_student=='on':
				ta.enroll_student=True
			else:
				ta.enroll_student=False
			create_assignment=request.POST.get('create_assignment')
			if create_assignment=='on':
				ta.create_assignment=True
			else:
				ta.create_assignment=False

			ta.save()
			return redirect('viewta',pk)

	form=modifytaform()
	return render(request,'moodle/modifyta.html',{'form':form, 'user':ak})


@login_required(login_url='login')
def viewSubmissionta(request,pk,ak):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	assignment=Assignment.objects.filter(course=course,name=ak)
	assignment=assignment[0]
	submissions=Submission.objects.filter(assignment=assignment)
	return render(request,'moodle/viewsubmissionsta.html',{'submissions':submissions,'pk':course.title,'ak':assignment.name,'assignment':assignment})



@login_required(login_url='login')
def announcement(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	anns=Announcements.objects.filter(course=course)

	ins=False

	if request.user==course.user:
		ins=True

	tas=False
	if Ta.objects.filter(course=course,user=request.user).exists():
		tas=True

	form=Announcementform()

	if request.method == 'POST':
		form1=Announcementform(request.POST)
		if form1.is_valid():
			mess=request.POST.get('message')
			an=Announcements(course=course,message=mess)
			an.save()
			cous=Coursesundertaken.objects.filter(title=pk)
			emails=list()
			for cou in cous:
				emails.append(cou.user.email)

			send_mail(
				'New announcement made in '+ pk,
				'Your instructor made a new announcement in the course '+pk+' , \n Below is the announcement \n'+mess,
				'1457205saikiran@gmail.com',
				emails,
				)
			return render(request,'moodle/Announcements.html',{'form':form,'anns':anns,'pk':pk,'ins':ins,'tas':tas})
		else:
			return render(request,'moodle/Announcements.html',{'form':form,'anns':anns,'pk':pk,'ins':ins,'tas':tas})		

	
	return render(request,'moodle/Announcements.html',{'form':form,'anns':anns,'pk':pk,'ins':ins,'tas':tas})



@login_required(login_url='login')
def discussion(request,pk):
	course=Coursescreated.objects.filter(title=pk)
	course=course[0]
	form=discussionform()
	username=request.user.username
	mess=Discussion.objects.filter(course=course)

	if request.method == 'POST':
		form1=discussionform(request.POST)
		if form1.is_valid():
			message=request.POST.get('message')
			d=Discussion(user=request.user,course=course,message=message)
			d.save()
			return render(request,'moodle/disscussionform.html',{'form':form,'mess':mess,'username':username,'title':course.title})
		else:
			return render(request,'moodle/disscussionform.html',{'form':form,'mess':mess,'username':username,'title':course.title})


	return render(request,'moodle/disscussionform.html',{'form':form,'mess':mess,'username':username,'title':course.title})


@login_required(login_url='login')
def listchat(request):
	users=User.objects.all()
	loginuser=request.user
	return render(request,'moodle/listchat.html',{'users':users,'loginuser':loginuser})


from django.db.models import Q

@login_required(login_url='login')
def chat(request,ak):
	user=User.objects.get(username=ak)
	form=chatform()
	chas=chats.objects.filter(Q(sender=request.user,receiver=user) | Q(sender=user,receiver=request.user)).order_by('date_created')

	if request.method =='POST':
		form1=chatform(request.POST)
		if form1.is_valid():
			message=request.POST.get('message')
			mes=chats(sender=request.user,receiver=user,message=message)
			mes.save()
			return render(request,'moodle/chat.html',{'form':form,'user':user,'chas':chas})
		else:
			return render(request,'moodle/chat.html',{'form':form,'user':user,'chas':chas})			

	return render(request,'moodle/chat.html',{'form':form,'user':user,'chas':chas})

