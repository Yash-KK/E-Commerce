from django import forms
from django import forms

# Model
from .models import (
    Account
)


class RegisterationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    class Meta:
        model = Account
        fields =['first_name', 'last_name', 'email', 'phone_number', 'password']
    
    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
    def __init__(self, *args, **kwargs):
        super(RegisterationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your Phone Number'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })    