from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Record
from django import forms
from .models import Booking
from datetime import date

# User Registration form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


# Record creation form
class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city']



#Update Record Form
class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model= Record
        fields =['first_name', 'last_name', 'email', 'phone', 'address', 'city']


class BookingForm(forms.ModelForm):
    # This field uses the HTML5 'date' input type for a native calendar/date picker
    booking_date = forms.DateField(
        label='Select Visit Date',
        widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
        initial=date.today
    )

    class Meta:
        model = Booking
        fields = ['booking_date', 'adult_tickets', 'child_tickets',  'customer_name', 'email']
        widgets = {
            # Ensure ticket counts can't be negative
            'adult_tickets': forms.NumberInput(attrs={'min': 1, 'max': 50}), 
            'child_tickets': forms.NumberInput(attrs={'min': 0, 'max': 50}),
           
        }

    def clean(self):
        """Custom validation to ensure at least one ticket is selected."""
        cleaned_data = super().clean()
        adults = cleaned_data.get('adult_tickets', 0)
        children = cleaned_data.get('child_tickets', 0)
     

        # Check that the sum of tickets is greater than zero
        if adults + children  == 0:
            raise forms.ValidationError("You must select at least one ticket to proceed.")

        return cleaned_data
