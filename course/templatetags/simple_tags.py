from django import template
import math
from course.models import UserCourse 

register = template.Library()
@register.simple_tag
def sellprice(price,discount):
    if discount is None or discount is 0:
        return price
    sellprice = price
    sellprice = price -(price * discount * 0.01)
    return math.floor(sellprice)

@register.filter
def money(price):
    return f'${price}'

@register.simple_tag
def is_enrolled(request,course):
    user = None
    if not request.user.is_authenticated:
        return False
    
    user = request.user
    try:
        usercourse  = UserCourse.objects.get(user=user,course=course) 
        return True

    except:
        return False

   
    
