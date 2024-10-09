from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from eLearningApp.models import Course, Profile, ContactMessage

from datetime import datetime, timedelta

import pandas as pd

def months_between(start_date, end_date):
    return (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days // 30

@staff_member_required
def admin_dashboard(request):
    # Courses by category
    courses_by_category = Course.objects.values('category').annotate(count=Count('id'))
    
    # Users registered over time
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    users_over_time = Profile.objects.filter(
        user__date_joined__range=[start_date, end_date]
    ).annotate(
        month=TruncMonth('user__date_joined')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Fill in missing months
    users_over_time = list(users_over_time)
    users_over_time = months_between(users_over_time, start_date, end_date, 'month', 'count')
    
    # Recent contact messages
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    
    # Top courses by enrollment
    top_courses = Course.objects.annotate(student_count=Count('students')).order_by('-student_count')[:5]
    
    context = {
        'courses_by_category': courses_by_category,
        'users_over_time': users_over_time,
        'recent_messages': recent_messages,
        'top_courses': top_courses,
    }
    
    return render(request, 'admin/dashboard.html', context)