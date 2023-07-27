from django import forms
from datetime import date, timedelta

class InputForm_must(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Calculate the start and end dates for the date range (7 days from today)
        today = date.today()
        end_date = today + timedelta(days=6)
        start_date = today
        self.fields['location'] = forms.CharField(label="*City Location", max_length=30)
        # Set the DateField widget's attributes to limit the date range
        self.fields['start_date'] = forms.DateField(
            label="Start Date",
            initial=start_date,
            widget=forms.DateInput(attrs={'type': 'date', 'min': start_date, 'max': end_date})
        )
        self.fields['end_date'] = forms.DateField(
            label="End Date",
            initial=end_date,
            widget=forms.DateInput(attrs={'type': 'date', 'min': start_date, 'max': end_date})
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than the start date.")

        return cleaned_data



class InputForm_not_must(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Calculate the start and end dates for the date range (7 days from today)
        today = date.today()
        end_date = today + timedelta(days=6)
        start_date = today
        self.fields['location_not_must'] = forms.CharField(label="City Location", max_length=30, required=False)
        # Set the DateField widget's attributes to limit the date range
        self.fields['start_date_not_must'] = forms.DateField(
            label="Start Date",
            initial=start_date,
            widget=forms.DateInput(attrs={'type': 'date', 'min': start_date, 'max': end_date})
        )
        self.fields['end_date_not_must'] = forms.DateField(
            label="End Date",
            initial=end_date,
            widget=forms.DateInput(attrs={'type': 'date', 'min': start_date, 'max': end_date})
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        #if end_date < start_date:
            #raise forms.ValidationError("End date cannot be earlier than the start date.")

        return cleaned_data
