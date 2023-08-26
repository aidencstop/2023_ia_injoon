from django.db import models


# Create your models here.
class Attendance(models.Model):
    # We declared each variable as 'Field'
    # each Field has type, such as Char, Integer, Date.
    # If we try to input data which is not appropriate with the field, Django denies it.
    # So this 'Field' system provides validation process.
    member_id = models.CharField(max_length=4)
    date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    workout_duration = models.IntegerField(null=True, blank=True)

    # Following series of setVar() functions are made to set variables' value indirectly by user.
    # This is a way to implement "Encapsulation"
    # each function gets value which is to be new value for a variable in object.
    # then the function changes the value accordingly.
    # user cannot change the value of variables in objects by themselves.
    # instead, these functions do.
    def setCheckInTime(self, check_in_time):
        self.check_in_time = check_in_time
        self.save()

    def setCheckOutTime(self, check_out_time):
        self.check_out_time = check_out_time
        self.save()

    def setWorkoutDuration(self, workout_duration):
        self.workout_duration = workout_duration
        self.save()

    def __str__(self):
        return str(self.date) + ": " + str(self.member_id)
