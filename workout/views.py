from .models import Workout
from member.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

# Create your views here.
@csrf_exempt
def manage_workout(request, member_id):
    if request.method == 'POST':
        if 'to_member_list' in request.POST:
            return redirect('/member/member_list/')
        if 'initialize' in request.POST:
            return redirect('/workout/manage_workout/'+member_id+'/')
        if 'save' in request.POST:

            workouts = Workout.objects.all().order_by('date')
            member_workouts = [a for a in workouts if a.member_id == member_id]

            workout_list = request.POST.getlist('workout')
            num_of_sets_list = request.POST.getlist('num_of_sets')
            weight1_list = request.POST.getlist('weight1')
            weight2_list = request.POST.getlist('weight2')
            weight3_list = request.POST.getlist('weight3')
            weight4_list = request.POST.getlist('weight4')
            weight5_list = request.POST.getlist('weight5')
            reps1_list = request.POST.getlist('reps1')
            reps2_list = request.POST.getlist('reps2')
            reps3_list = request.POST.getlist('reps3')
            reps4_list = request.POST.getlist('reps4')
            reps5_list = request.POST.getlist('reps5')
            for idx in range(len(member_workouts)):
                # pk = pk_list[idx]
                # date = date_list[idx]
                workout = workout_list[idx]
                num_of_sets = num_of_sets_list[idx]
                weight1 = int(weight1_list[idx])
                weight2 = int(weight2_list[idx])
                weight3 = int(weight3_list[idx])
                weight4 = int(weight4_list[idx])
                weight5 = int(weight5_list[idx])
                weight_list = [weight1, weight2, weight3, weight4, weight5]
                weight_list = json.dumps(weight_list)
                reps1 = int(reps1_list[idx])
                reps2 = int(reps2_list[idx])
                reps3 = int(reps3_list[idx])
                reps4 = int(reps4_list[idx])
                reps5 = int(reps5_list[idx])
                reps_list = [reps1, reps2, reps3, reps4, reps5]
                reps_list = json.dumps(reps_list)

                try:
                    member_workout = member_workouts[idx]
                    member_workout.workout = workout
                    member_workout.num_of_sets = num_of_sets
                    member_workout.weight_list = weight_list
                    member_workout.reps_list = reps_list
                    member_workout.save()
                except Exception:
                    continue

            return redirect('/workout/manage_workout/'+member_id+'/')

    member = User.objects.get(member_id=member_id)
    workouts = Workout.objects.all().order_by('date')
    member_workouts = [a for a in workouts if a.member_id == member_id]
    weight_lists = [json.loads(a.weight_list) for a in member_workouts]
    reps_lists = [json.loads(a.reps_list) for a in member_workouts]
    cnt_lists = [i + 1 for i in range(len(member_workouts))]
    data_list = zip(cnt_lists, member_workouts, weight_lists, reps_lists)
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'admin7.html',
        {
            'today':today,
            'user': member,
            'data_list': data_list
        }
    )
