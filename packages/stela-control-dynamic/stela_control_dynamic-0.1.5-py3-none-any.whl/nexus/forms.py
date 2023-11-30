from django import forms

from stela_control.models import Contact, Support, ChatSupport

class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['option','message','terms', 'image']


class ReadOnlySupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['option','message','terms', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["option"].disabled = True
        self.fields["message"].disabled = True
        self.fields["terms"].disabled = True

class ReadOnlySupportFormCostumer(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['option','message','terms']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["option"].disabled = True
        self.fields["message"].disabled = True
        self.fields["terms"].disabled = True

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comments
#         fields = ['name','email', 'message']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'].widget.attrs.update(
#             {'class': 'form-control w-100', 'placeholder': 'Your Name is?'})
#         self.fields['email'].widget.attrs.update(
#             {'class': 'form-control w-100', 'placeholder': 'Place Email'})
#         self.fields['message'].widget.attrs.update(
#             {'class': 'form-control w-100', 'placeholder': 'Your Message'})
        

        

