from django import forms
from multiupload.fields import MultiFileField
from .models import All_profiles, Image, VictimLifecycleEntry
from bootstrap_datepicker_plus.widgets import DatePickerInput
from home.models import home_profiles

class AllProfileForm(forms.ModelForm):
    pickup_date = forms.DateField(widget=DatePickerInput())
    images = MultiFileField(min_num=1, max_num=30, max_file_size=1024*1024*5)

    class Meta:
        model = All_profiles
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If the instance is not provided, the form is in create mode
        if not self.instance.pk:
            self.fields['ngo_assigned'].choices = self.get_home_choices()

    def get_home_choices(self):
        return [(home.home_name, home.home_name) for home in home_profiles.objects.all()]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        for image in self.cleaned_data['images']:
            Image.objects.create(all_profile=instance, image=image)

        return instance

class VictimLifecycleEntryForm(forms.ModelForm):
    class Meta:
        model = VictimLifecycleEntry
        fields = ['entry_text', 'attachment']