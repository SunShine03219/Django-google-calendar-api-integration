from django import forms
class MeetingForm(forms.Form):
    metting_name = forms.CharField(max_length=200)
    metting_date = forms.DateField()
    metting_start_time = forms.TimeField()
    metting_end_time = forms.TimeField()