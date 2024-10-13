from django import forms
from .models import Lead, Agent


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class LeadModelForm(forms.ModelForm):

    agent = forms.ModelChoiceField(
        Agent.objects, required=False
    )  # adding a model choice field

    class Meta:
        model = Lead
        fields = ("first_name", "last_name", "age", "agent")
