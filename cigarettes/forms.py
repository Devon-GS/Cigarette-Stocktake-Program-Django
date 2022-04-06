from django import forms

class UplaodFileForm(forms.form):
    file = forms.FileField()
    