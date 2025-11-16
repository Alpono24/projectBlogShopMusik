from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # сразу авторизуем пользователя
            # return redirect('blog:posts')  # Перенаправляем на главную страницу блога
            return render(request, 'successful_registration.html')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})