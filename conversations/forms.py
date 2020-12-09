from django import forms


class AddMessage(forms.Form):
    message = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Write your message here"}),
    )
