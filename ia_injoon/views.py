from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.
@csrf_exempt
def main(request):
    if request.method == 'POST': # 버튼 눌러졌을 때만 작동하는 if문
        if 'to_member_login' in request.POST:
            return redirect('/member/member_login/')
        if 'to_admin_login' in request.POST:
            return redirect('/member/admin_login/')
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)
    today = target_year + '.' + target_month + '.' + target_day
    return render(
        request,
        'main.html',
        {
            'today': today
        }
    )
