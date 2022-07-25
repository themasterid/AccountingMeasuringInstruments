from django import forms

from .models import Materials


class TbMaterialGrCreateEditForm(forms.ModelForm):
    """
    Форма создания/редактирования материала.
    """

    class Meta:
        model = Materials
        fields = [
            'number_sap', 'material', 'material_text', 'quantity',
            'date_commissioning', 'end_of_service_date',
            'manufacturer', 'inventory_number', 'test_date',
            'test_result', 'date_next_testst', 'expiration_date',
            'date_disposal', 'is_active', 'is_blocked', 'date_of_inspection',
            'date_next_inspection', 'inspection_result', ]
        widgets = {
            'number_sap': forms.Select(
                attrs={'class': 'form-select'}),
            'material': forms.Select(
                attrs={'class': 'form-select'}),
            'material_text': forms.Select(
                attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'}),
            'date_commissioning': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }),
            'end_of_service_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'readonly': 'readonly'}),
            'date_of_inspection': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }),
            'date_next_inspection': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'readonly': 'readonly'}),
            'manufacturer': forms.Select(
                attrs={'class': 'form-control'}),
            'inventory_number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'}),
            'test_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
            'test_result': forms.Select(
                attrs={'class': 'form-control'}),
            'inspection_result': forms.Select(
                attrs={'class': 'form-control'}),
            'date_next_testst': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'readonly': 'readonly', }),
            'expiration_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'}),
            'date_disposal': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
        }
