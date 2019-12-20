from django.contrib import admin
from django.urls import path
from client import views
 
urlpatterns = [
    path('', views.index),
    path('create', views.create),
    path('create_accidents', views.create_accidents),
    path('create_date', views.create_date),
    path('create_location', views.create_location),
    path('create_casualty', views.create_casualty),
    path('create_vehicles', views.create_vehicles),

    path('delete', views.delete_by_id),

    path('update', views.update),
    path('update_accidents', views.update_accidents),
    path('update_date', views.update_date),
    path('update_location', views.update_location),
    path('update_casualty', views.update_casualty),
    path('update_vehicles', views.update_vehicles),

    path('select1', views.select1),
    path('select2', views.select2),
    path('select3', views.select3),
    path('select4', views.select4),
    path('select5', views.select5),

    path('window1', views.window1),
    path('window2', views.window2),
    path('window3', views.window3),
    # path('window4', views.window4),
    # path('window5', views.window5),

    path('view1', views.view1),
    path('view2', views.view2),
    path('view3', views.view3),
    path('view4', views.view4),
    path('view5', views.view5),

    path('procedure1', views.procedure1),
    path('procedure2', views.procedure2),
    path('procedure3', views.procedure3),
    path('procedure4', views.procedure4),
    path('procedure5', views.procedure5),

]
