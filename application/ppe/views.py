import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TbMaterialGrCreateEditForm
from .models import (DivisionOne, DivisionThree, DivisionTwo, Materials,
                     TbComplect, TbMaterial, TbMaterialGr, TbZavod)


def get_material(material_id):
    """
    Get and return material by ID for edit, update, destroy.
    """

    return Materials.objects.get(id=material_id)


def get_all_objects(obj):
    """
    Get and return material by ID for edit, update, destroy.
    """

    return obj.objects.all()


@login_required
def index(request):
    """
    View all Personal Protective Equipment.
    """

    divisions1 = get_all_objects(DivisionOne)
    materials = get_all_objects(Materials)
    tbcomplect_all = get_all_objects(TbComplect)
    tbzavod_all = get_all_objects(TbZavod)
    tbmaterial_all = get_all_objects(TbMaterial)
    materials_all = get_all_objects(TbMaterialGr)

    form_materials = TbMaterialGrCreateEditForm(
        request.POST or None)

    context = {
        'tbzavod_all': tbzavod_all,
        'tbmaterial_all': tbmaterial_all,
        'TbComplect_all': tbcomplect_all,
        'materials_all': materials_all,
        'materials': materials,
        'form_materials': form_materials,
        'divisions1': divisions1,
    }
    templates = 'ppe/index.html'
    return render(request, templates, context)


@login_required
def create(request):
    """
    Добавление нового материала в систему.
    """

    form_materials = TbMaterialGrCreateEditForm(
        request.POST or None)
    if form_materials.is_valid():
        item = form_materials.save(commit=False)
        years = datetime.timedelta(int(item.expiration_date) * 365)
        month = datetime.timedelta(int(item.expiration_date) * 24)
        item.date_of_block = timezone.now()
        item.end_of_service_date = (
            item.date_commissioning + years)
        # ! добавить месяц
        item.date_next_testst = (
            item.date_commissioning + month)
        # ! добавить осмотры сроки
        item.date_next_inspection = (
            item.date_commissioning + month)
        item.author = request.user
        item.save()
        msg1 = 'Материал создан!'
        messages.info(request, msg1)
        return redirect('ppe:index')

    materials = get_all_objects(Materials)
    template = 'ppe/index.html'
    context = {
        'materials': materials,
        'form_materials': form_materials, }
    return render(request, template, context)


@login_required
def edit(request, material_id):
    """
    Редактирование материала по id в системе.
    """

    material = get_object_or_404(
        Materials,
        id=material_id)
    if request.user != material.author or material.is_blocked:
        msg1 = 'Материал заблокирован!'
        messages.info(request, msg1)
        return redirect('ppe:index')

    old_data = material
    form_materials = TbMaterialGrCreateEditForm(
        request.POST or None,
        instance=material)

    if form_materials.is_valid() and request.user == material.author:
        item = form_materials.save(commit=False)
        years = datetime.timedelta(int(item.expiration_date) * 365)
        month = datetime.timedelta(int(item.expiration_date) * 24)
        item.login_of_block = request.user
        item.is_blocked = True
        item.date_of_block = timezone.now()
        item.end_of_service_date = (
            item.date_commissioning + years)
        # ! добавить месяц
        item.date_next_testst = (
            item.date_commissioning + month)
        # ! добавить осмотры сроки
        item.date_next_inspection = (
            item.date_commissioning + month)
        item.author = request.user
        item.save()
        msg2 = 'Материал отредактирован!'
        messages.info(request, msg2)
        return redirect('ppe:index')

    materials = get_all_objects(Materials)

    material_id = get_material(material_id)

    form_materials = TbMaterialGrCreateEditForm(instance=old_data)
    template = 'ppe/index.html'
    context = {
        'materials': materials,
        'material_id': material_id,
        'form_materials': form_materials,
        'is_edit': True}
    return render(request, template, context)


@login_required
def destroy(request, material_id):
    """
    Удаление материала автором и если он не имеет блокировку.
    """

    material = get_material(material_id)
    if request.user != material.author or material.is_blocked:
        msg1 = 'Материал заблокирован! Удалить нельзя!'
        messages.info(request, msg1)
        return redirect('ppe:index')

    material.delete()
    msg2 = 'Материал удален!'
    messages.info(request, msg2)
    return redirect('ppe:index')


@login_required
def removelock(request, material_id):
    """
    Remove the lock by ID Personal Protective Equipment.
    """

    material = get_material(material_id)

    if request.user == material.author and material.is_blocked:
        (
            material.date_of_block,
            material.login_of_block,
            material.is_blocked
        ) = None, None, False
        material.save()
        msg1 = 'Блокировка снята!'
        messages.info(request, msg1)
        return redirect('ppe:index')
    elif request.user != material.author and material.is_blocked:
        msg2 = (
            'Снять блокировку может только: '
            f'{material.login_of_block}')
        messages.info(request, msg2)
        return redirect('ppe:index')
    msg3 = 'Материал не заблокирован!'
    messages.info(request, msg3)
    return redirect('ppe:index')


def get_division_info(request, obj, division):
    method_get = request.method == 'GET'
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if method_get and is_ajax:
        pk = request.GET.get(division)
        try:
            volumes = get_object_or_404(obj, pk=pk)
        except Exception:
            return JsonResponse({"success": False}, status=400)
        user_info = {
            "name": volumes.name,
            "number_team_members": volumes.number_team_members,
            "responsible_accounting_ppe": volumes.responsible_accounting_ppe,
            "position": volumes.position,
            "complete_set": volumes.complete_set,
        }
        return JsonResponse({"user_info": user_info}, status=200)
    return JsonResponse({"success": False}, status=400)


def get_division_info2(request):
    """Получаем информацию AJAX."""

    return get_division_info(
        request, DivisionTwo, 'division2')


def get_division_info3(request):
    """Получаем информацию AJAX."""

    return get_division_info(
        request, DivisionThree, 'division3')


def load_division_one(request):
    pk = request.GET.get('division1')
    pk = not pk.isdigit() or pk
    divisions1 = DivisionTwo.objects.filter(
        division_two=pk).all()
    template = 'ppe/division/sp1.html'
    return render(
        request,
        template,
        {'divisions1': divisions1})


def load_division_two(request):
    pk = request.GET.get('division2')
    pk = not pk.isdigit() or pk
    divisions2 = DivisionThree.objects.filter(
        division_three=pk).all()
    template = 'ppe/division/sp2.html'
    return render(
        request,
        template,
        {'divisions2': divisions2})
