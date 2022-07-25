from django.contrib import admin
from django.urls import include, path
from ppe import views as divisions

urlpatterns = [
    path('', include('ppe.urls')),
    path('admin/', admin.site.urls),

    path(
        'ajax/get_division_info2',
        divisions.get_division_info2,
        name='get_division_info2'),
    path(
        'ajax/get_division_info3',
        divisions.get_division_info3,
        name='get_division_info3'),

    path(
        'ajax/load_division_one/',
        divisions.load_division_one,
        name='ajax_load_division_one'),  # AJAX
    path(
        'ajax/load_division_two/',
        divisions.load_division_two,
        name='ajax_load_division_two'),  # AJAX
    # path(
    #     'ajax/load_division_three/',
    #     divisions.load_division_three,
    #     name='ajax_load_division_three'),  # AJAX
]
