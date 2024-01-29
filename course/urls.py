
from django.urls import path
from . import views

urlpatterns = [
    path("",views.homeView.as_view()),
    path("base",views.base),
    path('course/<str:slug>',views.coursepage),
    path("signup",views.SignupView.as_view()),
    path("login",views.LoginView.as_view()),
    path("signout",views.signout),
    path('checkout/<str:slug>/',views.checkout , name = "checkout"),
    path('verify_payment',views.verify_payment),
    path('MyCourses',views.MyCourses.as_view()),
    path('search',views.search),
    path('contact',views.contact),
    
]