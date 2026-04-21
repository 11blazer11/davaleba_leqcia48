from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
 
 
class CustomRegisterForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. +995 555 123 456'}),
        label='Phone Number'
    )
 
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        label='I am a...',
        widget=forms.RadioSelect
    )
 
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'user_type', 'password1', 'password2')
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data.get('phone')
        user.user_type = self.cleaned_data.get('user_type')
        if commit:
            user.save()
        return user
 