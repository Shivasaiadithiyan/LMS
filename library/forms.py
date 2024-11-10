from django import forms
from django.contrib.auth.models import User
from . import models

# class ContactusForm(forms.Form):
#     Name = forms.CharField(max_length=30)
#     Email = forms.EmailField()
#     Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))




class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']



class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']


class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['enrollment','branch']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['name','isbn','author','category']
        

from django import forms
from . import models
from datetime import date

from django import forms
from . import models


class IssuedBookForm(forms.Form):
    # Select student by their enrollment number
    enrollment2 = forms.ModelChoiceField(
        queryset=models.StudentExtra.objects.all(),
        empty_label="Name and Enrollment",
        to_field_name="enrollment",  # using enrollment for selection
        label="Student"
    )
    
    # Select book by ISBN
    isbn2 = forms.ModelChoiceField(
        queryset=models.Book.objects.all(),
        empty_label="Book Name and ISBN",
        to_field_name="isbn",  # using isbn for selection
        label="Book"
    )
