from django import forms

class ExampleForm(forms.Form):
    n_samples = forms.IntegerField(label='Number of Samples', initial=200)
    lambda_value = forms.FloatField(label='Lambda Value', initial=1.0)
    alpha_value = forms.FloatField(label='Alpha Value', initial=1.0)
