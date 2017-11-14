from django import forms

class GitForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()
    gitrepo = forms.CharField()
    branch = forms.CharField()
