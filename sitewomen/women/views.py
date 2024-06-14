from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from women.forms import UploadFileForm
from women.models import Women, TagPost, UploadFiles

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


# def index(request):
#     posts = Women.published.all().select_related("cat")
#
#     data = {
#         "title": "Главная страница",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": 0,
#     }
#     return render(request, "women/index.html", context=data)


class WomenHome(ListView):
    model = Women
    template_name = "women/index.html"
    context_object_name = "posts"
    extra_context = {
        "title": "Главная страница",
        "menu": menu,
        "cat_selected": 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related("cat")

    # template_name = "women/index.html"
    #
    # extra_context = {
    #     "title": "Главная страница",
    #     "menu": menu,
    #     "posts": Women.published.all().select_related("cat"),
    #     "cat_selected": 0,
    # }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["title"] = "Главная страница"
    #     context["menu"] = menu
    #     context["posts"] = Women.published.all().select_related("cat")
    #     context["cat_selected"] = int(self.request.GET.get("cat_id", 0))
    #     return context


# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()
    data = {
        "title": "О сайте",
        "menu": menu,
        "form": form,
    }
    return render(request, "women/about.html", data)


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     data = {
#         "title": post.title,
#         "menu": menu,
#         "post": post,
#         "cat_selected": 1,
#     }
#     return render(request, "women/post.html", data)


class ShowPost(DetailView):
    # model = Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["post"].title
        context["menu"] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #     # print(form.cleaned_data)
#             #     try:
#             #         Women.objects.create(**form.cleaned_data)
#             #         return redirect("home")
#             #     except Exception:
#             #         form.add_error(None, "Error adding post!")
#             form.save()
#             return redirect("home")
#     else:
#         form = AddPostForm()
#
#     data = {
#         "title": "Добавление статьи",
#         "menu": menu,
#         "form": form,
#     }
#     return render(request, "women/addpage.html", data)


class AddPage(CreateView):
    # form_class = AddPostForm
    model = Women
    fields = "__all__"
    template_name = "women/addpage.html"
    # success_url = reverse_lazy("home")
    extra_context = {
        "title": "Добавление статьи",
        "menu": menu,
    }


class UpdatePage(UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    extra_context = {
        "title": "Редактирование статьи",
        "menu": menu,
    }


class DeletePage(DeleteView):
    model = Women
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    extra_context = {
        "title": "Удаление статьи",
        "menu": menu,
    }


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             "title": "Добавление статьи",
#             "menu": menu,
#             "form": form,
#         }
#         return render(request, "women/addpage.html", data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
#         data = {
#             "title": "Добавление статьи",
#             "menu": menu,
#             "form": form,
#         }
#         return render(request, "women/addpage.html", data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related("cat")
#
#     data = {
#         "title": "Отображение по рубрикам",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": category.pk,
#     }
#     return render(request, "women/index.html", context=data)


class WomenCategory(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        context["title"] = "Category - " + cat.name
        context["menu"] = menu
        context["cat_selected"] = cat.pk
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=1).select_related("cat")
#
#     data = {
#         "title": tag.tag,
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": None,
#     }
#
#     return render(request, "women/index.html", context=data)


class TagPostList(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        context["title"] = "Tag:" + tag.tag
        context["menu"] = menu
        context["cat_selected"] = None
        return context
