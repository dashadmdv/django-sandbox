from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse

menu = ["О сайте", "Добавить статус", "Обратная связь", "Войти"]


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "float": 28.56,
        "lst": [1, 2, "abc", True],
        "set": {1, 2, 3, 4, 5},
        "dict": {"key_1": "value_1", "key_2": "value_2"},
        "obj": MyClass(10, 20),
    }
    return render(request, "women/index.html", context=data)


def about(request):
    data = {"title": "О сайте"}
    return render(request, "women/about.html", data)


def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")


def categories_by_slug(request, cat_slug):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")


def archive(request, year):
    if year > 2024:
        uri = reverse("cats", args=("music",))
        return redirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
