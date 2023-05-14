from django import forms
from django.contrib.auth.forms import UserCreationForm
from store.models import User,ProductReview



class UserRegisterForm(UserCreationForm):
        username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
        email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
        password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
        password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
        
        class Meta:
            model=User
            fields=['username',
                    'email']
            
            
class ProductReviewForm(forms.ModelForm):
        review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write review'}))
        class Meta:
                model=ProductReview
                fields=['review','rating']