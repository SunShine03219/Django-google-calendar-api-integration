from django import forms
from .models import Project


class NewProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__" 
        exclude = ['pr_stakeholder', 'pr_provider','chatID', 'engaged_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoryL1': forms.TextInput(attrs={'class': 'form-control'}),
            'categoryL2': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'creation_date': forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'deadline_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'id': 'tags-input', 'readonly': 'readonly'}),
            'file': forms.FileInput(attrs={'class': 'form-control btn btn-primary', 'accept': 'application/pdf'}),
        }
        
    def clean_title(self):
        title_value = self.cleaned_data['title']
        return title_value.upper()
