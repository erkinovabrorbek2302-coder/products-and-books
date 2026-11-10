from django import forms
from .models import Comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email manzilingiz")
    first_name = forms.CharField(max_length=30, required=True, label="Ismingiz")
    last_name = forms.CharField(max_length=30, required=True, label="Familiyangiz")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'email', 'body']
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100, label="Sizning ismingiz")
    email = forms.EmailField(label="Sizning emailingiz")
    to = forms.EmailField(label="Kimga yuborish")
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Qo'shimcha izoh"
    )
