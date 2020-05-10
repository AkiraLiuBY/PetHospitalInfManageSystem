from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    ManagerID = forms.CharField(
        label='帐号',
        max_length=9,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    PassWord = forms.CharField(
        label='密码',
        max_length=20,
        widget=forms.TextInput(attrs={'class':'fomr=control'})
        
    )
    captcha = CaptchaField(
        label='验证码',
        required=True,
        error_messages={
            'required':'验证码不能为空'
        }
    )
