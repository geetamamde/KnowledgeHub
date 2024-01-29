from django.contrib import admin
from course.models import  Course ,Tag ,Prerequisite,Learning,Video,UserCourse,Payment,ContactUs
from django.utils.html import format_html
# Register your models here.

class TagAdmin(admin.TabularInline):
    model = Tag

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite

class LearningAdmin(admin.TabularInline):
    model = Learning

class VideoAdmin(admin.TabularInline):
    model =  Video


class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin , PrerequisiteAdmin ,LearningAdmin, VideoAdmin]

class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['order_id','get_user','course','status']
    list_filter = ['status']

    def get_user(self,payment):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")
    
    get_user.short_description = "USER"


admin.site.register(Course,CourseAdmin)
admin.site.register(Video)
admin.site.register(UserCourse)
admin.site.register(ContactUs)
admin.site.register(Payment,PaymentAdmin)

