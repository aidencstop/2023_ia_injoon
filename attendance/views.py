from .models import Attendance
from member.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.
@csrf_exempt
def manage_attendance(request, member_id):
    if request.method == 'POST':
        if 'to_member_list' in request.POST:
            return redirect('/member/member_list/')
        if 'initialize' in request.POST:
            user = User.objects.get(member_id=member_id)
            attendances = Attendance.objects.all().order_by('date')
            member_attendances = [a for a in attendances if a.member_id == member_id]
            return render(
                request,
                'admin6.html',
                {
                    'user': user,
                    'attendances': member_attendances
                }
            )
        if 'save' in request.POST:
            user = User.objects.get(member_id=member_id)
            attendances = Attendance.objects.all().order_by('date')
            member_attendances = [a for a in attendances if a.member_id == member_id]
            # pk_list = request.POST.getlist('pk')
            # date_list = request.POST.getlist('date')
            check_in_time_list = request.POST.getlist('check_in_time')
            check_out_time_list = request.POST.getlist('check_out_time')
            workout_duration_list = request.POST.getlist('workout_duration')
            #TODO: check_out_time, workout_duration이 없는 경우를 예외처리 해야함
            # print(len(member_attendances)==len(check_out_time_list))
            for idx in range(len(member_attendances)):
                # pk = pk_list[idx]
                # date = date_list[idx]
                member_attendance = member_attendances[idx]
                check_in_time = check_in_time_list[idx]
                check_out_time = check_out_time_list[idx]
                workout_duration = workout_duration_list[idx]
                try:
                    attendance = member_attendance
                    attendance.check_in_time = check_in_time
                    attendance.check_out_time = check_out_time
                    attendance.workout_duration = workout_duration
                    attendance.save()
                except Exception:
                    continue
            user = User.objects.get(member_id=member_id)
            attendances = Attendance.objects.all().order_by('date')
            member_attendances = [a for a in attendances if a.member_id == member_id]
            return render(
                request,
                'admin6.html',
                {
                    'user': user,
                    'attendances': member_attendances
                }
            )

    user = User.objects.get(member_id=member_id)
    attendances = Attendance.objects.all().order_by('date')
    member_attendances = [a for a in attendances if a.member_id == member_id]

    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'admin6.html',
        {
            'today':today,
            'user': user,
            'attendances': member_attendances
        }
    )
