from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views 

urlpatterns = [
    path('', views.home,name="home"),
    path('login/',views.loginPage,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.logoutPage,name="logout"),
    path('updatepassword/',views.reset,name="reset"),
    path('createcourse/',views.createcourse,name="createcourse"),
    path('joincourse/',views.joincourse, name="joincourse"),
    path('yourcourses/',views.yourcourse, name="yourcourse"),
    path('coursesundertaken/',views.joinedcourse, name="joinedcourse"),
    path('instructor/<str:pk>/',views.instructor,name="instructor"),
    path('student/<str:pk>/',views.student,name="student"),
    path('assignment/<str:pk>/',views.createAss,name="assignment"),
    path('viewsubmissions/<str:pk>/<str:ak>/',views.viewSubmission,name="viewsubmissions"),
    path('viewsubmissionsta/<str:pk>/<str:ak>/',views.viewSubmissionta,name='viewSubmissionta'),
    path('feedback/<str:pk>/<str:ak>/<str:sk>/',views.feedform,name="feedback"),
    path('viewassignment/<str:pk>/<str:ak>/',views.viewassignment, name="viewassignment"),
    path('addta/<str:pk>/',views.addTa,name='addTa'),
    path('enroll/<str:pk>',views.enroll,name='enroll'),
    path('tacourses/',views.tacourses,name='tacourses'),
    path('viewtacourses/<str:pk>/',views.viewtacourses,name='viewtacourses'),
    path('viewtas/<str:pk>/',views.viewta,name='viewta'),
    path('modifytas/<str:pk>/<str:ak>/',views.modifyta,name='modifyta'),
    path('Announcements/<str:pk>/',views.announcement,name='announcement'),
    path('discussionform/<str:pk>/',views.discussion,name='discussion'),
    path('viewchats/',views.listchat,name='listchat'),
    path('chat/<str:ak>/',views.chat,name='chat'),
    path('grades/<str:pk>/',views.grade,name='grade'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)