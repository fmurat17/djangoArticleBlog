from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article, Comment
from django.contrib.auth.decorators import login_required
# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles" : articles})
    articles = Article.objects.all()
    return render(request, "articles.html", {"articles" : articles})

def index(request):
    context = {
        "number1" : 5,
        "number2" : 7,
        "number3" : 10
    }
    return render(request, template_name = "index.html", context = context)

def about(request):
    context = {
        "numbers" : [1,2,3,4,5]
    }
    return render(request, template_name = "about.html", context = context)

@login_required(login_url = "user:login2")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request, "dashboard.html", context)
    
@login_required(login_url = "user:login2")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale Başarıyla Oluşturuldu")
        return redirect("index")
    return render(request, "addarticle.html", {"form" : form})

def detail(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all()
    return render(request, "detail.html", {"article" : article, "comments" : comments})

@login_required(login_url = "user:login2")
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale Başarıyla Güncellendi")
        return redirect("index")

    return render(request, "update.html", {"form" : form})
@login_required(login_url = "user:login2")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    messages.success(request, "Makale Başarıyla Silindi")
    return redirect("article:dashboard")

def addComment(request, id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author") # inputun name ini aldık
        comment_content = request.POST.get("comment_content") # text_area nın name ini aldık

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
    return redirect("/articles/article/" + str(id))
    #return redirect(reverse("article:deatil", kwargs = {"id":id}))
