from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def main(request):
    if request.method == 'POST':
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
