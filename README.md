# moodle

Below are the requirements for running the server

python 3.9.7

libraries:-

asgiref==3.4.1
cycler==0.11.0
Django==3.2.8
fonttools==4.28.2
gunicorn==20.1.0
kiwisolver==1.3.2
matplotlib==3.5.0
numpy==1.21.4
packaging==21.3
Pillow==8.4.0
pyparsing==3.0.6
python-dateutil==2.8.2
pytz==2021.3
setuptools-scm==6.3.2
six==1.16.0
sqlparse==0.4.2
tomli==1.2.2
whitenoise==5.3.0

pip install django (will do it after having the python 3.9.7)

Heroku deploy-
https://phoenix-moodle.herokuapp.com/
This is the link for the heroku deployed website although we have a slight issue while mailing.

key features:-

Courses:-
	One can create a course or join a course. A instructor can send invitations that contain the coursecode for other users to join the course, a student can view the percentage of course completed.

Assingments:-
	Instructor for the course can create assignment (including file upload, deadline, weightage), All the students will be notified through email.

TA's:-
	Each course enables a choice for the instructor to add the TA(Teaching assiasnt) who assist the instructor in various ways like creating assignment, enroll students, annocements. A instructor can change the previleges for a TA 

ToDo list:-
	Each student will have a Todo list which lists all the pending assignments for student and like wise all the pending evalutions for the instructor.

Communication:-
	Disscussion forums, annocements for course are created that enables a better way of communication. personal DM's are also created which enables users to chat with other users.

Statistics:-
	Course statistics and assignment statics for each course and assignment are displayed 

Evalution:-
	A Instructor can give feedback and grade to each submission. Also a instructor or TA can upload a csv file which contains name grade feedback for mass evalution.

Password update:-
	A user can update his/her password with OTP sent to the mail. 