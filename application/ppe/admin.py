from django.contrib import admin

from .models import (DivisionOne, DivisionThree, DivisionTwo, Materials,
                     TbComplect, TbMaterGrNorm, TbMaterial, TbMaterialGr,
                     TbNapr, TbRezult, TbStatusMatJur, TbZavod)


@admin.register(DivisionOne)
class DivisionOneAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'id',
        'name',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(DivisionTwo)
class DivisionTwoAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'id',
        'division_two',
        'name',
        'number_team_members',
        'responsible_accounting_ppe',
        'position',
        'complete_set',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(DivisionThree)
class DivisionThreeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'id',
        'division_three',
        'name',
        'number_team_members',
        'responsible_accounting_ppe',
        'position',
        'complete_set',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(TbNapr)
class TbNaprAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'IdNapr',
        'Napr',
        'SortNapr',
    )
    search_fields = ('IdNapr', 'Napr', 'SortNapr',)
    list_filter = ('IdNapr', 'Napr', 'SortNapr',)
    empty_value_display = '-пусто-'


@admin.register(TbRezult)
class TbRezultAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'Idisp',
        'NameRez',
    )
    search_fields = ('Idisp', 'NameRez',)
    list_filter = ('Idisp', 'NameRez',)
    empty_value_display = '-пусто-'


@admin.register(TbStatusMatJur)
class TbStatusMatJurAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'IdStatus',
        'NameStatus',
    )
    search_fields = ('IdStatus', 'NameStatus',)
    list_filter = ('IdStatus', 'NameStatus',)
    empty_value_display = '-пусто-'


@admin.register(TbZavod)
class TbZavodAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'Id_zavod',
        'Name_zavod',
        'Prizn_zav',
    )
    search_fields = ('Id_zavod', 'Name_zavod',)
    list_filter = ('Id_zavod', 'Name_zavod',)
    empty_value_display = '-пусто-'


@admin.register(TbMaterGrNorm)
class TbMaterGrNormAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'NumberCompl',
        'IdCompl',
        'IdMaterialGr',
        'KolMater',
        'IdPravilo',
        'IdNapr',
    )
    search_fields = ('IdCompl', 'IdMaterialGr',)
    list_filter = ('IdCompl', 'IdMaterialGr',)
    empty_value_display = '-пусто-'


@admin.register(TbComplect)
class TbComplectAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'IdComplect',
        'NumberCompl',
        'NameCompl',
    )
    search_fields = ('IdComplect', 'NumberCompl', 'NameCompl',)
    list_filter = ('IdComplect', 'NumberCompl', 'NameCompl',)
    empty_value_display = '-пусто-'


@admin.register(TbMaterial)
class TbMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'IdMaterialGr',
        'NameMaterSap',
        'NomSap',
        'SrokSlGod',
        'PlanIspMes',
        'PriznIsp',
        'NameMaterUn',
        'PriznUn',
        'PriznKol',
    )
    search_fields = ('IdMaterialGr', 'NameMaterSap',)
    list_filter = ('IdMaterialGr', 'NameMaterSap',)
    empty_value_display = '-пусто-'


@admin.register(TbMaterialGr)
class TbMaterialGrAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'IdMaterialGr',
        'NameMaterialGr',
        'IdEdIzm',
    )
    search_fields = ('IdMaterialGr', 'NameMaterialGr',)
    list_filter = ('IdMaterialGr', 'NameMaterialGr',)
    empty_value_display = '-пусто-'


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'number_sap',
        'material',
        'material_text',
        'quantity',
        'date_commissioning',
        'end_of_service_date',
        'manufacturer',
        'inventory_number',
        'test_date',
        'test_result',
        'date_of_inspection',
        'date_next_inspection',
        'inspection_result',
        'date_next_testst',
        'expiration_date',
        'date_disposal',
        'name_status',
        'is_active',
        'is_blocked',
        'date_of_block',
        'login_of_block',
        'group',
    )
    search_fields = ('material',)
    list_filter = ('material',)
    empty_value_display = '-пусто-'


# ! НА УДАЛЕНИЕ!
# @admin.register(TbPodr)
# class TbPodrAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk', 'NamePodrazd1', 'NamePodrazd2', 'NamePodrazd3',
#     )
#     search_fields = ('NamePodrazd1', 'NamePodrazd2', 'NamePodrazd3',)
#     list_filter = ('NamePodrazd1', 'NamePodrazd2', 'NamePodrazd3',)
#     empty_value_display = '-пусто-'
