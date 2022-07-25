# from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

RESULT_YES = 'Годен'
RESULT_NO = 'Не годен'

RESULT_CHOICES = (
    (RESULT_YES, RESULT_YES),
    (RESULT_NO, RESULT_NO),
)

RESULT_YES_E = 'Эксплуатация'
RESULT_NO_E = 'Выведен из эксплуатации'

RESULT_CHOICES_E = (
    (RESULT_YES_E, RESULT_YES_E),
    (RESULT_NO_E, RESULT_NO_E),
)

ED_IZM = '1'

ED_CHOICES = (
    (ED_IZM, 'шт.'),
)


class Materials(models.Model):
    """
    Список всех материалов в системе.
    """

    def get_inventory_number():
        """
        Выводим инвентарный номер.
        """

        all_materials = Materials.objects.all()
        number = len(all_materials)
        for _ in all_materials:
            inv_n = int(_.inventory_number)
            if inv_n > number:
                number = inv_n + 1
        number += 1
        return '{:07d}'.format(number)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор записи',)
    number_sap = models.ForeignKey(
        'TbMaterial',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        to_field='IdMaterial',
        related_name='number_sap',
        verbose_name='Номер SAP',)
    material = models.ForeignKey(
        'TbMaterialGr',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # to_field='IdMaterialGr',
        related_name='material',
        verbose_name='Материал',)
    material_text = models.ForeignKey(
        'TbMaterial',
        to_field='IdMaterial',
        on_delete=models.CASCADE,
        related_name='textmaterial',
        null=True,
        blank=True,
        verbose_name='Краткий текст',)
    quantity = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000)],
        verbose_name='Кол-во',)
    date_commissioning = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        # default=timezone.now,
        verbose_name='Дата ввода в эксплуатацию')
    end_of_service_date = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        # default=timezone.now,
        verbose_name='Дата окончания срока службы')
    manufacturer = models.ForeignKey(
        'TbZavod',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Завод изготовитель',)
    inventory_number = models.CharField(
        max_length=7,
        unique=True,
        default=get_inventory_number,
        verbose_name='Инвентарный номер',)
    test_date = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        # default=timezone.now,
        verbose_name='Дата испытания')
    test_result = models.CharField(
        max_length=9,
        # default=RESULT_CHOICES[1],
        null=True,
        blank=True,
        choices=RESULT_CHOICES,
        verbose_name='Результат испытания',)
    date_of_inspection = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        # default=timezone.now,
        verbose_name='Дата осмотра')
    date_next_inspection = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        # default=timezone.now,
        verbose_name='Дата следующего осмотра')
    inspection_result = models.CharField(
        max_length=100,
        # default=RESULT_CHOICES[1],
        null=True,
        blank=True,
        choices=RESULT_CHOICES,
        verbose_name='Результат осмотра',)
    date_next_testst = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name='Дата следующего испытания')
    expiration_date = models.CharField(
        max_length=15,
        default=3,
        verbose_name='Срок годности',)
    date_disposal = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name='Дата выбытия')
    name_status = models.ForeignKey(
        'TbRezult',
        null=True,
        default=True,
        on_delete=models.CASCADE,
        verbose_name='Статус',)
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен')
    is_blocked = models.BooleanField(
        default=False,
        verbose_name='В блоке')
    date_of_block = models.DateField(
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name='Дата блокировки')
    login_of_block = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='block_user',
        verbose_name='Логин блокировки')
    group = models.ForeignKey(
        'DivisionThree',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='group',
        verbose_name='СП 3-го уровня'
    )

    class Meta:
        verbose_name = 'Материал (созданы)'
        verbose_name_plural = 'Материалы (созданы)'
        ordering = ('id',)

    def __str__(self):
        return f'{self.material}'


class TbMaterialGr(models.Model):
    """
    ТБ группы материалов.
    """

    IdMaterialGr = models.IntegerField(
        unique=True,
        blank=True,
        verbose_name='ID материала группы')
    NameMaterialGr = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Материал')
    IdEdIzm = models.CharField(
        blank=True,
        max_length=10,
        default='шт.',
        choices=ED_CHOICES,
        verbose_name='Ед. изм.')
    # ! добавить вывод количества материалов
    number_materials = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Количество материалов')

    class Meta:
        verbose_name = 'Материал группы (Выгрузка)'
        verbose_name_plural = 'Материалы групп (Выгрузка)'
        ordering = ('id',)

    def __str__(self):
        return self.NameMaterialGr


class TbMaterial(models.Model):
    """
    Все материалы в системе.
    """

    IdMaterial = models.IntegerField(
        unique=True,
        verbose_name='ID материала')
    NameMaterSap = models.CharField(
        max_length=256,
        verbose_name='Краткий текст материла')
    IdMaterialGr = models.ForeignKey(
        TbMaterialGr,
        to_field='IdMaterialGr',
        on_delete=models.CASCADE,
        verbose_name='Материал')
    SrokSlGod = models.CharField(
        max_length=6,
        verbose_name='Срок службы, лет')
    PlanIspMes = models.CharField(
        max_length=5,
        verbose_name='План испытания, мес.')
    NomSap = models.CharField(
        max_length=10,
        verbose_name='Номер SAP')
    NameMaterUn = models.CharField(
        blank=True,
        max_length=128,
        verbose_name='Наименование универсальности',)
    PriznUn = models.BooleanField(
        verbose_name='Признак универсальности v[да]',)
    PriznIsp = models.BooleanField(
        verbose_name='Признак испытания v[да]',)
    PriznKol = models.BooleanField(
        verbose_name='Признак колличества v[да]',)

    class Meta:
        verbose_name = 'Все материалы (Выгрузка)'
        verbose_name_plural = 'Все материалы (Выгрузка)'
        ordering = ('id',)

    def __str__(self):
        return self.NameMaterSap


class TbComplect(models.Model):
    """
    ТБ комплект.
    """

    IdComplect = models.IntegerField(
        unique=True,
        verbose_name='ID комплекта')
    NumberCompl = models.IntegerField(
        unique=True,
        verbose_name='Номер комплекта')
    NameCompl = models.TextField(
        unique=True,
        max_length=1024,
        verbose_name='Наименование комплекта')

    class Meta:
        verbose_name = 'Норма материала (Выгрузка)'
        verbose_name_plural = 'Нормы материалов (Выгрузка)'
        ordering = ('IdComplect',)

    def __str__(self):
        return self.NameCompl


class TbMaterGrNorm(models.Model):
    """
    Нормы группы материалов.
    """

    IdMaterNorm = models.IntegerField(
        unique=True,
        verbose_name='ID материала норма')
    IdCompl = models.ForeignKey(
        'TbComplect',
        to_field='IdComplect',
        on_delete=models.SET_NULL,
        related_name='complect',
        null=True,
        verbose_name='ID комплекта')
    NumberCompl = models.IntegerField(
        default=1,
        verbose_name='Номер комплекта ')
    IdMaterialGr = models.ForeignKey(
        'TbMaterialGr',
        to_field='IdMaterialGr',
        on_delete=models.SET_NULL,
        related_name='mater',
        null=True,
        verbose_name='Группа материала',)
    KolMater = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        verbose_name='Количество материала',)
    IdPravilo = models.CharField(
        max_length=6,
        null=True,
        verbose_name='ID правило')
    IdNapr = models.CharField(
        # 'ppe.TbNapr',
        # to_field='IdNapr',
        # on_delete=models.PROTECT,
        # related_name='napr',
        # default=1,
        max_length=6,
        null=True,
        blank=True,
        verbose_name='Напряжение')

    class Meta:
        verbose_name = 'ТБ материала нормы группа (Выгрузка)'
        verbose_name_plural = 'ТБ материалов нормы группы (Выгрузка)'
        ordering = ('id',)

    def __str__(self):
        return str(self.IdCompl)


class TbZavod(models.Model):
    """
    Список уникальных заводов.
    """

    Id_zavod = models.IntegerField(
        unique=True,
        verbose_name='ID завода')
    Name_zavod = models.CharField(
        unique=True,
        max_length=512,
        verbose_name='Наименование заводов-изготовителей',)
    Prizn_zav = models.BooleanField(
        default=True,
        verbose_name='Признак v[нет поставок]')

    class Meta:
        verbose_name = 'Завод изготовитель (Выгрузка)'
        verbose_name_plural = 'Заводы изготовители (Выгрузка)'
        ordering = ('id',)

    def __str__(self):
        return self.Name_zavod


class TbStatusMatJur(models.Model):
    """
    Статусы эксплуатации.
    - Эксплуатация
    - Выведен из эксплуатации
    """

    IdStatus = models.IntegerField(
        unique=True,
        verbose_name='ID статус',
    )
    NameStatus = models.CharField(
        max_length=50,
        verbose_name='Наименование статуса',)

    class Meta:
        verbose_name = 'Статус (Выгрузка)'
        verbose_name_plural = 'Статусы (Выгрузка)'
        ordering = ('id',)

    def __str__(self):
        return self.NameStatus


class TbRezult(models.Model):
    """
    Результаты испытаний
    - Годен
    - Не годен
    """

    Idisp = models.IntegerField(
        unique=True,
        verbose_name='ID испытания')
    NameRez = models.CharField(
        max_length=9,
        verbose_name='Наименование испытания',)

    class Meta:
        verbose_name = 'Результат испытания (Выгрузка)'
        verbose_name_plural = 'Результаты испытания (Выгрузка)'
        ordering = ('id',)

    def __str__(self):
        return self.NameRez


class TbNapr(models.Model):
    """
    Напряжения, список.
    """
    IdNapr = models.IntegerField(
        unique=True,
        verbose_name='ID напряжения')
    Napr = models.CharField(
        unique=True,
        max_length=512,
        verbose_name='Напряжение',)
    SortNapr = models.IntegerField(
        unique=True,
        verbose_name='Сорт напяржения')

    class Meta:
        verbose_name = 'Напряжение (Выгрузка)'
        verbose_name_plural = 'Напряжения (Выгрузка)'
        ordering = ('id',)

    def __str__(self):
        return self.Napr


class DivisionOne(models.Model):
    """Подразделение СП-1 го уровня."""

    name = models.CharField(
        max_length=512,
        verbose_name='СП 1-го уровня',)

    class Meta:
        verbose_name = 'СП 1-го уровня'
        verbose_name_plural = 'СП 1-го уровня'
        ordering = ['id']

    def __str__(self):
        return self.name


class DivisionTwo(models.Model):
    """Подразделение СП-2 го уровня."""

    division_two = models.ForeignKey(
        DivisionOne,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='СП 1-го уровня'
    )
    name = models.CharField(
        max_length=1024,
        verbose_name='СП 2-го уровня',
    )
    number_team_members = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)],
        verbose_name='Количество членов бригады',
    )
    responsible_accounting_ppe = models.CharField(
        max_length=256,
        default='Ivanov',
        verbose_name='Ответственный за учет СИЗ',
    )
    position = models.CharField(
        max_length=256,
        default='Engineer',
        verbose_name='Должность',
    )
    complete_set = models.CharField(
        max_length=256,
        default='Complect',
        verbose_name='Комплект',
    )

    class Meta:
        verbose_name = 'СП 2-го уровня'
        verbose_name_plural = 'СП 2-го уровня'
        ordering = ['id']

    def __str__(self):
        return (f'{self.division_two} -> {self.name}')


class DivisionThree(models.Model):
    """Подразделение СП-3 го уровня."""

    division_three = models.ForeignKey(
        DivisionTwo,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='СП 2-го уровня',
    )
    name = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name='СП 3-го уровня'
    )
    number_team_members = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)],
        verbose_name='Количество членов бригады',
    )
    responsible_accounting_ppe = models.CharField(
        max_length=256,
        default='Ivanov',
        verbose_name='Ответственный за учет СИЗ',
    )
    position = models.CharField(
        max_length=256,
        default='Engineer',
        verbose_name='Должность',
    )
    complete_set = models.CharField(
        max_length=256,
        default='Complect',
        verbose_name='Комплект',
    )

    class Meta:
        verbose_name = 'СП 3-го уровня'
        verbose_name_plural = 'СП 3-го уровня'
        ordering = ['id']

    def __str__(self):
        return (f'{self.division_three} -> {self.name}')


# ! НА УДАЛЕНИЕ!
# class TbPodr(models.Model):
#     """
#     Список подразделений (удалить).
#     """

#     NamePodrazd1 = models.CharField(
#         blank=True,
#         max_length=512,
#         verbose_name='СП 1-го уровня',)
#     NamePodrazd2 = models.CharField(
#         blank=True,
#         max_length=512,
#         verbose_name='СП 2-го уровня',)
#     NamePodrazd3 = models.CharField(
#         blank=True,
#         max_length=512,
#         verbose_name='СП 3-го уровня',)

#     class Meta:
#         verbose_name = 'Подразделение (Выгрузка)'
#         verbose_name_plural = 'Подразделения (Выгрузка)'
#         ordering = ('id',)

#     def __str__(self):
#         return (
#             f'{self.NamePodrazd1} -> '
#             f'{self.NamePodrazd2} -> '
#             f'{self.NamePodrazd3}')
