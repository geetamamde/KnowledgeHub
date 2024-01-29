from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render , redirect
from .models import Course , Video ,Payment ,UserCourse,ContactUs
from .forms import CustomUserForm,LoginForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import logout ,login
from time import time
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from KnowledgeHub.settings import *
import razorpay
client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))
#for Email

from django.core.mail import send_mail
from django.core import mail
from django.conf import settings





def base(request):
    return render(request,"base.html",{})

def search(request): 
    query = request.GET['search']

    if len(query)>100:
        allcourse = Course.objects.none()
    else:
        allcourseTitle = Course.objects.filter(name__icontains = query )
        allcourseDesc = Course.objects.filter(desc__icontains = query )
        allcourse = allcourseTitle.union(allcourseDesc)
    if allcourse.count() ==0:
        messages.info(request, 'oops!.. seems like you need to try again')
    params = {'allcourse':allcourse ,'query':query}

    return render(request,"search.html",params)




class homeView(ListView):
  template_name = "home.html"
  queryset = Course.objects.filter(active=True)
    

def coursepage(request , slug):
    
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by('serial_number')

    if serial_number is None:
        serial_number = 1 

    video = Video.objects.get(serial_number = serial_number , course = course)
    
    if video.is_preview is False:

        if request.user.is_authenticated is False :
           return redirect('/login')
        else:
            user = request.user
            try:
                usercourse = UserCourse.objects.get(user = user  , course = course)
            except:
               return redirect('checkout', slug=course.slug)
            
    context ={
       'course': course,
        'video': video,
        'videos':videos,
        
    }
    return render(request,"particularcourse.html",context=context)

 
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request , form.cleaned_data)
        next_page = self.request.GET.get('next')
        if next_page is not None :
            return redirect(next_page)
        return super().form_valid(form)  


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = CustomUserForm
    success_url = '/login'

    def form_valid(self, form):
        user = form.save()

        subject = "Thank you"
        message = "Thank you for joining us...keep exploring keep learning."
        from_email = "knowledggehub@gmail.com"
        recipient_list = [form.cleaned_data['email']]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

def signout(request):
     logout(request)
     return redirect('/')

@login_required(login_url='/login')
def checkout(request,slug):
    course = Course.objects.get(slug=slug)
    user = request.user
    action = request.GET.get('action')
    order = None
    payment = None
    error = None
    try:
        user_course = UserCourse.objects.get(user=user,course=course) 
        error = "already enrolled"
        return redirect('/MyCourses')
    
    except:
        pass
    amount = None
    if error is None:
        amount = int((course.price -( course.price * course. discount *0.01)) *100)
    
    if amount == 0:
        usercourse = UserCourse(user = user , course =course)
        usercourse.save()
        return redirect('/MyCourses')

    if action =='Enroll_Now':
        currency = "INR"
        receipt = f"KnowledgeHub-{int(time())}"
        data = {"amount":amount,"currency": currency,"receipt":receipt}
        order = client.order.create(data=data)

        payment = Payment()
        payment.user = user
        payment.course = course
        payment.order_id = order.get('id')
        payment.save()

    return render(request,"checkout.html",{"course" : course,"order" : order ,"payment": payment ,"user":user,"error":error})

@csrf_exempt
def verify_payment(request):
    if request.method =='POST':
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = UserCourse(user = payment.user , course = payment.course)
            usercourse.save()

            payment.user_course = usercourse
            payment.save()
            messages.info(request, 'congratulations')
                
            return redirect('/MyCourses')
        except:
             return redirect('/login')


@method_decorator(login_required(login_url='login'),name='dispatch')
class MyCourses(ListView):
    template_name = 'mycourse.html'
    queryset = UserCourse.objects.all()
    context_object_name = 'user_course'

    def get_queryset(self) :
        return UserCourse.objects.filter(user = self.request.user)
    


def contact(request):
    if request.method == 'POST':
        fname = request.POST['name']
        femail = request.POST['email']
        fphonenumber = request.POST['phonenumber']
        fdescription = request.POST['description']

        query = ContactUs(name =fname,email = femail, phonenumber=fphonenumber,description=fdescription)
        query.save()
        messages.info(request,"we will get back you soon")
        return redirect('/contact')

    return render(request,"contact.html",{})
