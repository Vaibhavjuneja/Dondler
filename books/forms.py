from django import forms

class RelatedForm(forms.Form):
    subject=forms.CharField(max_length=500)
    field=forms.BooleanField(required=False)
