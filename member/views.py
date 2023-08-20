from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User
from attendance.models import Attendance
from workout.models import Workout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserChangeForm, CustomUserDeleteForm, AdminLoginForm
from django.contrib.auth.hashers import check_password
import datetime
import json
import pandas as pd
import numpy as np
import matplotlib
import os
from pathlib import Path



@csrf_exempt
def add_a_new_member(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/member/member_list/')
        if 'save' in request.POST:
            user = User.objects.create_user(
                member_id=request.POST['member_id'],
                name=request.POST['name'],
                age=request.POST['age'],
                gender=request.POST['gender'],
                registration_date=request.POST['registration_date'],
                phone_number=request.POST['phone_number'],
                athletic_experience=request.POST['athletic_experience'],
                expiration_date=request.POST['expiration_date'],
            )
            # auth.login(request, user)
            return redirect('/member/add_a_new_member/')
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(request, 'admin3.html',
        {
            'today':today
        }
    )


@csrf_exempt
def member_list(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/member/admin_login/')
        if 'add' in request.POST:
            return redirect('/member/add_a_new_member/')
        if 'restore' in request.POST:
            return redirect('/member/restore_members/')
        if 'remove' in request.POST:
            selected = request.POST.getlist('selected')
            for pk in selected:
                user = User.objects.get(pk=int(pk))
                # print(user.name)
                form = CustomUserDeleteForm(request.POST, instance=user)
                if form.is_valid():
                    # form.save()
                    user = form.save()  # 변경
                    user.is_active = False  # 변경
                    user.save()
        if 'edit' in request.POST:
            selected = request.POST.getlist('selected')
            print(selected)
            if len(selected)>1:
                pass
            elif len(selected)==1:
                pk = selected[0]
                user = User.objects.get(pk=pk)

                return redirect('/member/edit_member_info/'+pk+'/')
            else:
                pass

    users = User.objects.all().order_by('pk')
    active_users = [user for user in users if user.is_active]
    cnt_lists = [i + 1 for i in range(len(active_users))]
    data_list = zip(cnt_lists, active_users)
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'admin2.html',
        {
            'today': today,
            'data_list': data_list
        }
    )


@csrf_exempt
def edit_member_info(request, pk):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/member/member_list/')
        if 'save' in request.POST:
            user = User.objects.get(pk=pk)
            user.member_id=request.POST['member_id']
            user.name=request.POST['name']
            user.age=request.POST['age']
            user.gender=request.POST['gender']
            user.registration_date=request.POST['registration_date']
            user.phone_number=request.POST['phone_number']
            user.athletic_experience=request.POST['athletic_experience']
            user.expiration_date=request.POST['expiration_date']

            user.save()
            # form = CustomUserChangeForm(request.POST, instance=user)
            # if form.is_valid():
            #     form.save()

            return redirect('/member/edit_member_info/'+str(pk)+'/')


    user = User.objects.get(pk=pk)
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'admin4.html',
        {
            'today': today,
            'user': user
        }
    )


@csrf_exempt
def restore_members(request):
    if request.method == 'POST':
        if 'restore' in request.POST:
            selected = request.POST.getlist('selected')
            for pk in selected:
                user = User.objects.get(pk=int(pk))
                # print(user.name)
                form = CustomUserDeleteForm(request.POST, instance=user)
                if form.is_valid():
                    # form.save()
                    user = form.save()  # 변경
                    user.is_active = True  # 변경
                    user.save()
        if 'back' in request.POST:
            return redirect('/member/member_list/')

    users = User.objects.all().order_by('pk')
    deleted_users = [user for user in users if not user.is_active]
    cnt_lists = [i + 1 for i in range(len(deleted_users))]
    data_list = zip(cnt_lists, deleted_users)
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'admin5.html',
        {
            'today':today,
            'data_list': data_list
        }
    )


@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        # if 'to_main' in request.POST:
        #     return redirect('/')
        if 'login' in request.POST:
            member_id = request.POST['member_id']
            password = request.POST['password']
            try:
                user = User.objects.get(member_id=member_id)

                if check_password(password, user.password):
                    auth.login(request, user)
                    return redirect('/member/member_list/', {'user': user})
                else:
                    return redirect('/member/admin_login/')
            except Exception:
                pass
                # TODO:should deal with invalid user case

            return redirect('/member/admin_login/')
        if 'to_main' in request.POST:
            return redirect('/')
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'admin1.html',
        {
            'today':today
        }
    )

@csrf_exempt
def member_login(request):
    if request.method == 'POST':
        # if 'to_main' in request.POST:
        #     return redirect('/')
        if 'login' in request.POST:
            member_id = request.POST['member_id']
            try:
                user = User.objects.get(member_id=member_id)
                auth.login(request, user)

                return redirect('/member/check_in_or_out/', {'user': user})

            except Exception:
                return redirect('/member/member_login/')
        if 'to_main' in request.POST:
            return redirect('/')
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'member1.html',
        {
            'today':today
        }
    )


def check_in_or_out(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/member/member_login/')
        if 'checkin' in request.POST:
            user = auth.get_user(request)
            target_year=str(datetime.datetime.today().year)
            target_month=str(datetime.datetime.today().month)
            target_day=str(datetime.datetime.today().day)
            user_attendances = Attendance.objects.filter(member_id=user.member_id, date__year=target_year, date__month=target_month, date__day=target_day)
            if len(user_attendances)>0:
                #TODO: ban message
                return redirect('/member/check_in_or_out/', {'user': user})
            else:
                #date: 'YYYY-MM-DD'
                #time: 'HH:MM'
                now = datetime.datetime.now()
                attendance = Attendance.objects.create(
                    member_id=user.member_id,
                    date=target_year+'-'+target_month+'-'+target_day,
                    check_in_time=str(now.hour)+':'+str(now.minute),
                )
                return redirect('/member/check_in/', {'user': user})
        if 'checkout' in request.POST:
            user = auth.get_user(request)
            target_year = str(datetime.datetime.today().year)
            target_month = str(datetime.datetime.today().month)
            target_day = str(datetime.datetime.today().day)
            try:
                user_attendance = Attendance.objects.get(member_id=user.member_id, date__year=target_year, date__month=target_month, date__day=target_day)
                if user_attendance.check_out_time is None:
                    #TODO: update user's check_out_time and worout_duration
                    now = datetime.datetime.now()
                    user_attendance.check_out_time = str(now.hour)+':'+str(now.minute)
                    workout_duration = now.hour - user_attendance.check_in_time.hour
                    user_attendance.workout_duration = workout_duration
                    user_attendance.save()
                    return redirect('/member/check_out/', {'user': user})
                else:
                    # TODO: ban message(check-out exist already)
                    return redirect('/member/check_in_or_out/', {'user': user})
            except Exception:
                # TODO: ban message(no check-in record today)
                return redirect('/member/check_in_or_out/', {'user': user})
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year+'.'+target_month+'.'+target_day
    return render(
        request,
        'member2.html',
        {
            'today':today
        }
    )


def plot_recent_workouts(member_recent_workouts):
    result_list = [0, 0, 0, 0]
    category_name_list = ['Push', 'Pull', 'Leg', 'Core']
    if len(member_recent_workouts)==0:
        pass
    else:
        for member_recent_workout in member_recent_workouts:
            workout_category = int(Workout.workout_category_sm_level_dict[member_recent_workout.workout][0]) #0, 1, 2, 3
            weight_list = json.loads(member_recent_workout.weight_list) # [20, 20, 20, 20, 20]
            reps_list = json.loads(member_recent_workout.reps_list) # [5, 5, 5, 5, 5]
            sumproduct = 0
            for i in range(len(weight_list)):
                sumproduct += weight_list[i]*reps_list[i]
            result_list[workout_category]+=sumproduct

    df = pd.DataFrame(index=category_name_list, columns=['Value'])
    df['Value']=result_list
    figure = df.plot(kind='bar', legend=False).get_figure()

    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    figure.savefig(os.path.join(BASE_DIR, 'static')+"/image/figure.png")
    return figure


def check_in(request):
    if request.method == 'POST':
        if 'checkin' in request.POST:

            auth.logout(request)
            return redirect('/member/member_login/')
    user = auth.get_user(request)
    member_id = user.member_id
    workouts = Workout.objects.all().order_by('date')
    member_workouts = [a for a in workouts if a.member_id == member_id]
    member_recent_workouts = member_workouts[-10:]
    print(member_recent_workouts)
    plot = plot_recent_workouts(member_recent_workouts) # plot save in static/image/figure.png

    main_recommended_workout_name, main_recommended_weight_list, main_recommended_reps_list,\
        sub_recommended_workout_name, sub_recommended_weight_list, sub_recommended_reps_list = \
        Workout.get_recommendation(member_workouts)
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'member3.html',
        {
            'today':today,
            'user': user,

            'main_workout_name': main_recommended_workout_name,
            'main_recommended_weight_list': main_recommended_weight_list,
            'main_recommended_reps_list': main_recommended_reps_list,

            'sub_workout_name': sub_recommended_workout_name,
            'sub_recommended_weight_list': sub_recommended_weight_list,
            'sub_recommended_reps_list': sub_recommended_reps_list,
        }
    )


def check_out(request):
    if request.method == 'POST':
        if 'checkout' in request.POST:
            user = auth.get_user(request)
            member_id = user.member_id
            target_year = str(datetime.datetime.today().year)
            target_month = str(datetime.datetime.today().month)
            target_day = str(datetime.datetime.today().day)
            date = '-'.join([target_year, target_month, target_day])
            #TODO: check if input is valid(length of weight and reps same / valid workout name)

            main_workout_name = request.POST['main_workout']
            main_workout_weight_list = request.POST.getlist('main_weight')
            main_workout_num_of_sets = len(main_workout_weight_list)
            main_workout_weight_list = [int(a) for a in main_workout_weight_list]
            main_workout_weight_list = json.dumps(main_workout_weight_list)
            main_workout_reps_list = request.POST.getlist('main_reps')
            main_workout_reps_list = [int(a) for a in main_workout_reps_list]
            main_workout_reps_list = json.dumps(main_workout_reps_list)
            main_workout = Workout.objects.create(
                member_id=member_id,
                date=date,
                workout=main_workout_name,
                num_of_sets=main_workout_num_of_sets,
                weight_list=main_workout_weight_list,
                reps_list=main_workout_reps_list,
            )
            #TODO: create workout object as main_workout

            sub_workout_name = request.POST['sub_workout']
            sub_workout_weight_list = request.POST.getlist('sub_weight')
            sub_workout_num_of_sets = len(sub_workout_weight_list)
            sub_workout_weight_list = [int(a) for a in sub_workout_weight_list]
            sub_workout_weight_list = json.dumps(sub_workout_weight_list)
            sub_workout_reps_list = request.POST.getlist('sub_reps')
            sub_workout_reps_list = [int(a) for a in sub_workout_reps_list]
            sub_workout_reps_list = json.dumps(sub_workout_reps_list)
            sub_workout = Workout.objects.create(
                member_id=member_id,
                date=date,
                workout=sub_workout_name,
                num_of_sets=sub_workout_num_of_sets,
                weight_list=sub_workout_weight_list,
                reps_list=sub_workout_reps_list,
            )
            # TODO: create workout object as sub_workout

            auth.logout(request)
            return redirect('/member/member_login/')
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'member4.html',
        {
            'today':today
        }
    )
