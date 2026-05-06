from django import forms

from .models import Book


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
