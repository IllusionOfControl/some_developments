from django import forms


class CompanionNameForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )


class MessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "chat-message-input"
            }
        )
    )
