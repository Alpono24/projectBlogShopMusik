from allauth.account.views import login
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category
from .forms import PostForm



# Create your views here.

def posts(request):
    title = 'Статьи'
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    query = request.GET.get('q') #111
    posts = Post.objects.all().order_by(('-created_at'))
    if category_id:
        posts = posts.filter(category_id=category_id)
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        ).distinct()


    # Пагинация
    paginator = Paginator(posts, 10)  # показать по 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'title': title, 'categories': categories, 'page_obj': page_obj}
    return render(request, 'posts.html', context)



@login_required(login_url='/registration/login/')
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})


@login_required(login_url='/registration/login/')
def add_post(request):
    title = 'Страница добавления статьи'
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:posts')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form, 'title': title})



@login_required(login_url='/registration/login/')
def edit_post(request, id):
    title = 'Страница редактирования статьи'
    post = get_object_or_404(Post, id=id)
    if post.author != request.user and not request.user.is_superuser:
        return render(request, 'action_prohibited.html')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post, 'title': title})




@login_required(login_url='/registration/login/')
def delete_post(request, id):
    title = 'Подтверждение удаления'
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return render(request, 'action_prohibited.html')
    if request.method == 'POST':
        post.delete()
        return redirect('blog:posts')
    return render(request, 'delete_confirmation.html', {'post': post})



@login_required(login_url='/registration/login/')
def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')  # Получаем тему письма из формы
        message = request.POST.get('message')  # Получаем тело письма из формы
        recipient_list = ['alex.ponomarov@mail.ru']

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False
            )
            return render(request, 'email_sent_successfully.html')
        except Exception as e:
            return render(request, 'email_error.html', {'error_message': str(e)})
    else:
        return render(request, 'send_email.html')

