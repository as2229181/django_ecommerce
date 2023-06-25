from django import forms
from django.contrib.auth.forms import UserCreationForm
from store.models import User,ProductReview,Profile



class UserRegisterForm(UserCreationForm):
        username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
        email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
        password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
        password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
        
        class Meta:
            model=User
            fields=['username',
                    'email']
def get_profile(request):
        profile = Profile.objects.get(user=request.user)           
        return profile 

class ProductReviewForm(forms.ModelForm):
        review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write review'}))
        class Meta:
                model=ProductReview
                fields=['review','rating']




class ProfileForm(forms.ModelForm):
        full_name = forms.CharField( widget=forms.TextInput(attrs={"placeholder":"Full Name",'class':'form-control'}))
        introduction = forms.CharField(widget=forms.Textarea(attrs={"size": 500,"placeholder":"introduction",'class':'form-control'}))
        phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"phone",'class':'form-control'}))    
      
        class Meta:
               model = Profile 
               fields = ['full_name', 'image', "introduction", "phone"]                 