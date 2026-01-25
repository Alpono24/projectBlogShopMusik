from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category
from .forms import PostForm
from .tasks import send_email_async



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
    paginator = Paginator(posts, 5)
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
def send_email_back(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = ['alex.ponomarov@mail.ru']

        send_email_async.delay(subject, message, recipient_list)

        return render(request, 'email_sent_successfully.html')
    else:
        return render(request, 'send_email.html')