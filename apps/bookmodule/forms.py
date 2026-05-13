from django import forms

from .models import Address, Address2, Book, Student, Student2, StudentActivity


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'price', 'edition', 'quantity', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'required': True}),
            'author': forms.TextInput(),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'edition': forms.NumberInput(attrs={'min': '1'}),
            'quantity': forms.NumberInput(attrs={'min': '0'}),
            'rating': forms.NumberInput(attrs={'min': '1', 'max': '5'}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price

    def clean_edition(self):
        edition = self.cleaned_data['edition']
        if edition < 1:
            raise forms.ValidationError('Edition must be at least 1.')
        return edition

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city']
        widgets = {
            'city': forms.TextInput(attrs={'placeholder': 'Enter city name'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter student name'}),
            'age': forms.NumberInput(attrs={'min': '1'}),
        }


class Address2Form(forms.ModelForm):
    class Meta:
        model = Address2
        fields = ['city', 'street']
        widgets = {
            'city': forms.TextInput(attrs={'placeholder': 'Enter city name'}),
            'street': forms.TextInput(attrs={'placeholder': 'Enter street name'}),
        }


class Student2Form(forms.ModelForm):
    class Meta:
        model = Student2
        fields = ['name', 'age', 'addresses']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter student name'}),
            'age': forms.NumberInput(attrs={'min': '1'}),
            'addresses': forms.CheckboxSelectMultiple,
        }


class StudentActivityForm(forms.ModelForm):
    class Meta:
        model = StudentActivity
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Activity title'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
