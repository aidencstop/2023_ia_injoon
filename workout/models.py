from django.db import models
from django.contrib.postgres.fields import ArrayField
import json

# Create your models here.
class Workout(models.Model):
    member_id = models.CharField(max_length=4)
    date = models.DateField()
    workout = models.CharField(max_length=20)
    num_of_sets = models.IntegerField(default=5)
    weight_list = models.CharField(max_length=200, default='')
    reps_list = models.CharField(max_length=200, default='')

    workout_category_sm_level_dict = {
        #Push
        'Bent-Over Triceps Extension': '001', # Sub Hard
        'Cable Triceps Extension': '000',  # Sub Easy
        'Barbell Bench Press': '011', # Main Hard
        'Dumbbell Bench Press': '010', # Main Easy
        #Pull
        'Barbell Row': '101', # Sub Hard
        'Dumbbell Row': '100', # Sub Easy
        'Barbell Dead Lift': '111', # Main Hard
        'Dumbbell Dead Lift': '110', # Main Easy
        #Leg
        'Barbell Lunge': '201', # Sub Hard
        'Leg Extension': '200', # Sub Easy
        'Barbell Squat': '211', # Main Hard
        'Leg Press': '210',  # Main Easy
        #Core
        'Dumbbell Side Bend': '301', # Sub Hard
        'Cable Side Bend': '300', # Sub Easy
        'Cable Crunch': '311',  # Main Hard
        'AB Crunch Machine': '310',  # Main Easy
    }
    category_sm_level_workout_dict = {
        #Push
        '001': 'Bent-Over Triceps Extension',  # Sub Hard
        '000': 'Cable Triceps Extension',  # Sub Easy
        '011': 'Barbell Bench Press',  # Main Hard
        '010': 'Dumbbell Bench Press',  # Main Easy
        #Pull
        '101': 'Barbell Row',  # Sub Hard
        '100': 'Dumbbell Row',  # Sub Easy
        '111': 'Barbell Dead Lift',  # Main Hard
        '110': 'Dumbbell Dead Lift',  # Main Easy
        #Leg
        '201': 'Barbell Lunge',  # Sub Hard
        '200': 'Leg Extension',  # Sub Easy
        '211': 'Barbell Squat',  # Main Hard
        '210': 'Leg Press',  # Main Easy
        #Core
        '301': 'Dumbbell Side Bend',  # Sub Hard
        '300': 'Cable Side Bend',  # Sub Easy
        '311': 'Cable Crunch',  # Main Hard
        '310': 'AB Crunch Machine',  # Main Easy
    }

    @staticmethod
    def calculate_one_rm( weight_list, reps_list):
        rm_list = []
        for i in range(len(weight_list)):
            one_rm = weight_list[i]+(weight_list[i]*reps_list[i]*0.025)
            rm_list.append(one_rm)
        best_rm = max(rm_list)
        return best_rm

    @staticmethod
    def get_recommended_workout_category(workout_list):
        category_count_list = [0, 0, 0, 0]
        for workout in workout_list:
            category_count_list[int(Workout.workout_category_sm_level_dict[workout.workout][0])]+=1
        min_category_count = min(category_count_list)
        for idx, category_count in enumerate(category_count_list):
            if category_count==min_category_count:
                min_category=str(idx)
        return min_category



    @staticmethod
    def get_recommended_workout_program(workout_name, weight_list=None, reps_list=None):
        if weight_list is None:
            return workout_name, [13, 13, 13, 13, 13], [5, 5, 5, 5, 5]

        category = Workout.workout_category_sm_level_dict[workout_name][0]
        sm = Workout.workout_category_sm_level_dict[workout_name][1]
        level = Workout.workout_category_sm_level_dict[workout_name][2]

        rm = Workout.calculate_one_rm(weight_list, reps_list)

        if level=='1':
            recommended_weight=int(rm/2)
        else:
            if rm>100:
                workout_name = Workout.category_sm_level_workout_dict[category+sm+'1']
                recommended_weight = int((rm / 2)*0.8)
            else:
                recommended_weight = int(rm / 2)

        recommended_weight_list = [recommended_weight]*5
        recommended_reps_list = [5]*5

        return workout_name, recommended_weight_list, recommended_reps_list

    @staticmethod
    def get_recommendation(member_workouts):
        member_recent_workouts = member_workouts[-10:]

        recommended_workout_category = Workout.get_recommended_workout_category(member_recent_workouts)

        # main
        main_recommended_workout_record = None
        for member_workout in reversed(member_workouts):
            if Workout.workout_category_sm_level_dict[member_workout.workout][0:2] == recommended_workout_category+'1':
                main_recommended_workout_record = member_workout
                break
        if main_recommended_workout_record is None:
            workout_name = Workout.category_sm_level_workout_dict[recommended_workout_category + "10"]
            main_recommended_workout_name, main_recommended_weight_list, main_recommended_reps_list = \
                Workout.get_recommended_workout_program(workout_name)
        else:
            main_recommended_workout_name, main_recommended_weight_list, main_recommended_reps_list = \
                Workout.get_recommended_workout_program(main_recommended_workout_record.workout,
                                                        json.loads(main_recommended_workout_record.weight_list),
                                                        json.loads(main_recommended_workout_record.reps_list))
        # sub
        sub_recommended_workout_record = None
        for member_workout in reversed(member_workouts):
            if Workout.workout_category_sm_level_dict[member_workout.workout][0:2] == recommended_workout_category+'0':
                sub_recommended_workout_record = member_workout
                break
        if sub_recommended_workout_record is None:
            workout_name = Workout.category_sm_level_workout_dict[recommended_workout_category + "00"]
            sub_recommended_workout_name, sub_recommended_weight_list, sub_recommended_reps_list = \
                Workout.get_recommended_workout_program(workout_name)
        else:
            sub_recommended_workout_name, sub_recommended_weight_list, sub_recommended_reps_list = \
                Workout.get_recommended_workout_program(sub_recommended_workout_record.workout,
                                                        json.loads(sub_recommended_workout_record.weight_list),
                                                        json.loads(sub_recommended_workout_record.reps_list))

        return main_recommended_workout_name, main_recommended_weight_list, main_recommended_reps_list,\
            sub_recommended_workout_name, sub_recommended_weight_list, sub_recommended_reps_list

    def __str__(self):
        return str(self.date) + ": " + str(self.member_id)
