from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=30,null = False)
    slug = models.CharField(max_length=50,null = False , unique =True)
    desc = models.CharField(max_length=500)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False,default = 0)
    active = models.BooleanField(default = False)
    thumbnail = models.ImageField(upload_to="files/thumbnail")
    date = models.DateField(auto_now_add = True)
    resource= models.FileField(upload_to="files/resource")
    length = models.IntegerField(null=False)

    def __str__(self) :
        return self.name
    
class Property(models.Model):
    description = models.CharField(max_length=30,null = False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    
    class Meta :
        abstract = True

class Tag( Property):
    pass

class Prerequisite(Property):
    pass

class Learning(Property):
    pass


class Video(models.Model):
    title = models.CharField(max_length=100,null = False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length = 100)
    is_preview = models.BooleanField(default = False)
    
    def __str__(self) :
        return self.title
    
class UserCourse(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)

    def __str__(self) :
        return f'{self.user.username} - {self.course.name}'
    
class Payment(models.Model):
    order_id = models.CharField(max_length = 50 , null = False)
    payment_id = models.CharField(max_length = 50)
    user_course = models.ForeignKey(UserCourse , null = True , blank = True ,  on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)

class ContactUs(models.Model):
    
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=12)
    description = models.TextField()

   



   
