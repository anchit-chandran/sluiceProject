from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('inventory', views.inventory_list),
    path('detail/<int:id>', views.inventory_detail),
    path('reduce_stock/<int:id>', views.reduce_stock),
]

urlpatterns = format_suffix_patterns(urlpatterns)