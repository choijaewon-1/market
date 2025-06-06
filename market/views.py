from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Post
from .forms import PostForm

from django.core.paginator import Paginator

@login_required
def post_list(request):
    sort = request.GET.get('sort', 'latest')
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')

    posts = Post.objects.all()

    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))

    if category:
        posts = posts.filter(category=category)

    if sort == 'price_asc':
        posts = posts.order_by('price')
    elif sort == 'price_desc':
        posts = posts.order_by('-price')
    else:
        posts = posts.order_by('-created_at')

    # ✅ 페이지네이션: 한 페이지당 5개
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'market/post_list.html', {
        'posts': posts,
        'sort': sort,
        'category': category,
        'search': search,
    })


# ✅ 게시글 상세보기
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'market/post_detail.html', {'post': post})

# ✅ 게시글 작성
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'market/post_form.html', {'form': form})

# ✅ 게시글 수정
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("본인만 수정할 수 있습니다.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'market/post_form.html', {'form': form})

# ✅ 게시글 삭제
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("본인만 삭제할 수 있습니다.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'market/post_confirm_delete.html', {'post': post})

# ✅ 마이페이지 (내 글 목록)
@login_required
def my_page(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'market/my_page.html', {
        'user': request.user,
        'posts': posts
    })
