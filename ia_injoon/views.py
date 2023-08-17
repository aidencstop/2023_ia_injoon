from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def main(request):
    if request.method == 'POST': # 버튼 눌러졌을 때만 작동하는 if문
        if 'to_member_login' in request.POST:
            return redirect('/member/member_login/')
        if 'to_admin_login' in request.POST:
            return redirect('/member/admin_login/')

    return render(
        request,
        'main.html',
        {
        }
    )
