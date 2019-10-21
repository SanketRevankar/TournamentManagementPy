from django.shortcuts import redirect


def home(request):
    return redirect('Registration/')


def logout(request):
    request.session.clear()

    return redirect('/Registration')
