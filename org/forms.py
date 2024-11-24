from django import forms
from .models import Organization

class SubOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [ 'name', 'address', 'parent']  # Include necessary fields
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass the user to the form
        super().__init__(*args, **kwargs)
        if user:
            # Filter parent field to show only organizations created by the current user
            self.fields['parent'].queryset = Organization.objects.filter(created_by=user, is_main=True)
             
            
