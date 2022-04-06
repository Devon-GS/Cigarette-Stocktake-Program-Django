from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_items', views.add_items, name='add_items'),
    path('add_sales', views.add_sales, name='add_sales'),
    path('add_purchases', views.add_purchases, name='add_purchases'),
    path('calculate', views.calculate, name='calculate'),
    path('calculate_stock_on_hand', views.calculate_stock_on_hand, name='calculate_stock_on_hand'),
    path('csv_download', views.csv_download, name='csv_download'),
    path('clean_database', views.clean_database, name='clean_database'),
    path('reset_stock_levels', views.reset_stock_levels, name='reset_stock_levels'),
]
