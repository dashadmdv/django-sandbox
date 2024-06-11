from django.urls import path, re_path, register_converter

from . import views, converters

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path("", views.index),
    path("cats/<int:cat_id>/", views.categories),
    path("cats/<slug:cat_slug>/", views.categories_by_slug),
    re_path(r"^archive_reg/(?P<year>[0-9]{4})/", views.archive),
    path("archive/<yyyy:year>/", views.archive),
]
