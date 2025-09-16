from django import forms

class ExampleForm(forms.Form):
    """
    Example form for security testing.
    Demonstrates CSRF protection and input validation.
    """
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter book title',
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe the book...',
            'rows': 5,
            'class': 'form-control'
        }),
        required=False
    )

    def clean_title(self):
        """Custom validation to demonstrate secure input handling."""
        title = self.cleaned_data.get('title')
        if '<script>' in title.lower():
            raise forms.ValidationError("Invalid content detected.")
        return title.strip()