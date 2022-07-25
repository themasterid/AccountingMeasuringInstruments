from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'ppe'

urlpatterns = [
    path('logout/', LogoutView.as_view(
        template_name='users/logged_out.html'), name='logout'),
    path('login/', LoginView.as_view(
        template_name='users/login.html'), name='login'),

    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    # path('modules2/', views.get_division_two, name='division_two'),
    # path('modules3/', views.get_division_three, name='division_three'),

    path('create/', views.create, name='create'),
    path('edit/<int:material_id>/', views.edit, name='edit'),
    path('delete/<int:material_id>/', views.destroy, name='delete'),
    path('removelock/<int:material_id>/', views.removelock, name='removelock'),
]
