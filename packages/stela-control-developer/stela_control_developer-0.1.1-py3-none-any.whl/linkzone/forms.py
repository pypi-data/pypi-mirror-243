from django.utils.translation import gettext_lazy as _
from django import forms
from stela_control.models import (
    Contact, Addresses, City,
    Comments, ContactResponse
    )

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control w-100', 'placeholder': _('Your Name is?')})
        self.fields['subject'].widget.attrs.update(
            {'class': 'form-control w-100', 'placeholder': _('Subject')})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control w-100', 'placeholder': _('Place Email')})
        self.fields['message'].widget.attrs.update(
            {'class': 'form-control w-100', 'placeholder': _('Your Message')})
        self.fields['name'].label=False
        self.fields['subject'].label=False
        self.fields['email'].label=False
        self.fields['message'].label=False
        
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['host', 'status']

class ResponseContactForm(forms.ModelForm):
    class Meta:
        model = ContactResponse
        fields = ['message']

class ResponseContactFormDisabled(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].disabled = True

    class Meta:
        model = ContactResponse
        fields = ['message']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name','email', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control w-100', 'placeholder': _('Your Name is?')})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control w-100', 'placeholder': _('Place Email')})
        self.fields['message'].widget.attrs.update(
            {'class': 'form-control w-100', 'placeholder': _('Your Message')})
        
class AddressForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = ['country_address','city_address','address','phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_address'].queryset = City.objects.none()

        if 'country_address' in self.data:
            try:
                country_id = int(self.data.get('country_address'))
                self.fields['city_address'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city_address'].queryset = self.instance.country_address.city_set.all()
