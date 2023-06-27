from django.db import models


# Create your models here.
class Attendance(models.Model):
    member_id = models.CharField(max_length=4)
    date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    workout_duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.date) + ": " + str(self.member_id)

    # def create(self, member_id, date, check_in_time, check_out_time=None, workout_duration=None):
    #     """
    #     Create a new object with the given kwargs, saving it to the database
    #     and returning the created object.
    #     """
    #     obj = self.model(
    #         member_id=member_id,
    #         date=date,
    #         check_in_time=check_in_time,
    #     )
    #     self._for_write = True
    #     obj.save(force_insert=True, using=self.db)
    #     return obj
