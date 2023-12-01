from django import forms
import imghdr
from django.http import JsonResponse
import re, phonenumbers
from django.core.validators import URLValidator
from phonenumbers import geocoder, carrier
from .functions import caption_optimizer
from datetime import date, timedelta
from geolocation.models import City, Country
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from accounts.models import UserBase
from .models import (
        Newsletter, BillingRecipt, ItemProducts, ItemServices,ItemDiscount, 
        Templates, Content, Inventory, Modules, TemplateSections, StelaColors,
        Variants, Sizes, Gallery, Bulletpoints, VariantsImage, Wallet, DynamicBullets, 
        DataEmail, Category, SitePolicy, LegalProvision, Support, SupportResponse, ChatSupport, 
        FacebookPostPage, FacebookPageComments, FacebookPageCommentsReply,FacebookPageEvent, 
        FacebookPageLikes, FacebookPageMessages, FAQ, Contact, Comments, FacebookPageShares, 
        FacebookPostMedia, IGPost, ContactResponse, IGMediaContent, Company, SocialLinks, ImageGallery,
        SetFaq, Reviews, ProStelaExpert, LiteraryWork, Resource, BillFile
)
import re
#Support
class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['option','message','terms','image']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].widget.attrs.update(
                    {'class': 'form-control'})
            
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

#Billing 
class BillingForm(forms.ModelForm):
    class Meta: 
        model = BillingRecipt
        fields = ['report', 'option']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["report"].required = False

class BillingFormSuscription(forms.ModelForm):
    class Meta: 
        model = BillingRecipt
        fields = ['report']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["report"].required = False

class BillingChargeFormPOS(forms.ModelForm):
    class Meta:
        model = ItemProducts
        fields = ['field','qty']
      
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['field'].widget.attrs.update(
            {'class': 'form-control col-lg-8 mx-3 mb-4', 'placeholder': 'Field'})
        self.fields['qty'].widget.attrs.update(
            {'class': 'form-control col-lg-2 mx-3 mb-4', 'placeholder': 'qty'})
        self.fields['field'].label = False
        self.fields['qty'].label = False
        self.fields['field'].queryset = Variants.objects.filter(product__lang=self.request.LANGUAGE_CODE)

class BillingChargeFormDynamic(forms.ModelForm):
    class Meta:
        model = ItemServices
        fields = ['field','qty']
      
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['field'].widget.attrs.update(
            {'class': 'form-control col-lg-8 mx-3 mb-4', 'placeholder': 'Field'})
        self.fields['qty'].widget.attrs.update(
            {'class': 'form-control col-lg-2 mx-3 mb-4', 'placeholder': 'qty'})
        self.fields['field'].label = False
        self.fields['qty'].label = False
        self.fields['field'].required = True
        self.fields['qty'].required = True
        self.fields['field'].queryset = Modules.objects.filter(parent__owner=self.request.user, parent__yearly=False, parent__type="Service", parent__lang=self.request.LANGUAGE_CODE).order_by('parent').exclude(price=0)   

class BillingDiscountForm(forms.ModelForm):
    class Meta: 
        model = ItemDiscount
        fields = ['field','amount']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['field'].widget.attrs.update(
            {'class': 'form-control col-lg-8 mx-3 mb-4', 'placeholder': 'Field'})
        self.fields['amount'].widget.attrs.update(
            {'class': 'form-control col-lg-2 mx-3 mb-4', 'placeholder': 'amount'})
        self.fields['field'].label = False
        self.fields['amount'].label = False
        self.fields['field'].required = True
        self.fields['amount'].required = True

#invoiceCustom
class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
       super(RequiredFormSet, self).__init__(*args, **kwargs)
       for form in self.forms:
         form.empty_permitted = False

#developerLoad
class categForm(forms.ModelForm):

    class Meta: 
        model = Category
        exclude = ('slug', 'owner',)
        fields = '__all__'

class TempSecForm(forms.ModelForm):

    class Meta: 
        model = TemplateSections
        fields = ['section']

class StylesForm(forms.ModelForm):

    class Meta: 
        model = Content
        fields = ['parent', 'title', 'media']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
                {'class': 'form-control'})
        
class ColorsForm(forms.ModelForm):

    class Meta: 
        model = StelaColors
        exclude = ('owner',)
        fields = '__all__'

#inventory Product
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = True
        self.fields['image'].widget.attrs.update(
                    {'class': 'form-control'})
    class Meta:
        model = Inventory
        exclude = ('slug','owner','type','price','qty', 'sku', 'lang', 'id')
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = True
        self.fields['image'].widget.attrs.update(
                    {'class': 'form-control'})
    class Meta:
        model = Inventory
        exclude = ('slug','owner','type', 'sku', 'category', 'lang', 'id')
        fields = '__all__'

class ModulesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
                {'class': 'form-control'})
    class Meta:
        model = Modules
        exclude = ('parent',)
        fields = '__all__'

class VariantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Inventory.objects.filter(type="Product").order_by('title')
        self.fields['image'].widget.attrs.update(
                {'class': 'form-control'})
    class Meta:
        model = Variants
        fields = '__all__'
        exclude = ('id',)
    
class SizeForm(forms.ModelForm):

    class Meta:
        model = Sizes
        exclude = ('product','id')
        fields = '__all__'

class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        exclude = ('catalogue', 'id')
        fields = '__all__'

class BulletForm(forms.ModelForm):

    class Meta:
        model = Bulletpoints
        exclude = ('product', 'id')
        fields = '__all__'

class VariantImageForm(forms.ModelForm):

    class Meta:
        model = VariantsImage
        fields = '__all__'
        exclude = ('id',)

class TemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
                        {'class': 'form-control'})
    class Meta:
        model = Templates
        exclude = ('slug', 'id',)
        fields = '__all__'
    
#ContentStela (AboutSection, SliderSection, BoxSection, PortfolioSection, MediaSection, MisionSection, LegalSection, FooterSections, LinkSections)
class StelaAboutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
    class Meta:
        model = Content
        fields = ['title', 'content', 'media', 'status']

class AppstelaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
    class Meta:
        model = Content
        fields = ['appstela','subtitle','content','media','url', 'status'] 

class PathForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Content
        fields = ['path', 'content', 'status']

class MediaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
    class Meta:
        model = Content
        fields = ['media', 'url', 'status']

class FooterContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = False

    class Meta:
        model = Content
        fields = ['content', 'status', 'status']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class PolicyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False

    class Meta:
        model = SitePolicy
        fields = ['title','section','status']

class LegalProvitionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False

    class Meta:
        model = LegalProvision
        fields = ['clause', 'clause_content']

#SiteContent
class TextContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title','subtitle',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
           
    def clean_title(self):
        title = self.cleaned_data["title"]

        if not title:
            raise forms.ValidationError(_("The title is required."))
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data["subtitle"]

        if not subtitle:
            raise forms.ValidationError(_("The subtitle is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', subtitle):
            raise forms.ValidationError(_("The subtitle contains unauthorized characters."))

        return subtitle

    def clean_content(self):
        content = self.cleaned_data["content"]

        if not content:
            raise forms.ValidationError(_("The content is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', content):
            raise forms.ValidationError(_("The content contains unauthorized characters."))

        return content

class SimpleContentForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ['title','subtitle','media',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
            
    def clean_title(self):
        title = self.cleaned_data["title"]

        if not title:
            raise forms.ValidationError(_("The title is required."))
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data["subtitle"]

        if not subtitle:
            raise forms.ValidationError(_("The subtitle is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', subtitle):
            raise forms.ValidationError(_("The subtitle contains unauthorized characters."))

        return subtitle

    def clean_media(self):
        image = self.cleaned_data["media"]

        if not image:
            raise forms.ValidationError(_("The image container cannot be empty."))

        image_format = imghdr.what(image)
        if image_format not in ['jpeg', 'png']:
            raise forms.ValidationError(_("The image format is not valid. Only JPEG and PNG files are allowed."))

        return image
    
class ContentForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ['title','subtitle','media', 'content',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
            
    def clean_title(self):
        title = self.cleaned_data["title"]

        if not title:
            raise forms.ValidationError(_("The title is required."))
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data["subtitle"]

        if not subtitle:
            raise forms.ValidationError(_("The subtitle is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', subtitle):
            raise forms.ValidationError(_("The subtitle contains unauthorized characters."))

        return subtitle

    def clean_content(self):
        content = self.cleaned_data["content"]
        clean_content=caption_optimizer(content)
        
        if not content:
            raise forms.ValidationError(_("The content is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', clean_content):
            raise forms.ValidationError(_("The content contains unauthorized characters."))

        return content
    
    def clean_media(self):
        image = self.cleaned_data["media"]

        if not image:
            raise forms.ValidationError(_("The image container cannot be empty."))

        image_format = imghdr.what(image)
        if image_format not in ['jpeg', 'png']:
            raise forms.ValidationError(_("The image format is not valid. Only JPEG and PNG files are allowed."))

        return image

class AboutContentForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ['about','title','media', 'content',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
            
    def clean_title(self):
        title = self.cleaned_data["title"]

        if not title:
            raise forms.ValidationError(_("The title is required."))
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        return title

    def clean_content(self):
        content = self.cleaned_data["content"]
        clean_content=caption_optimizer(content)
        
        if not content:
            raise forms.ValidationError(_("The content is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', clean_content):
            raise forms.ValidationError(_("The content contains unauthorized characters."))

        return content
    
    def clean_media(self):
        image = self.cleaned_data["media"]

        if not image:
            raise forms.ValidationError(_("The image container cannot be empty."))

        image_format = imghdr.what(image)
        if image_format not in ['jpeg', 'png']:
            raise forms.ValidationError(_("The image format is not valid. Only JPEG and PNG files are allowed."))

        return image

class ContentDynamicForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ['media','title','subtitle','content','url',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
            
    def clean_title(self):
        title = self.cleaned_data["title"]
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        if not title:
            raise forms.ValidationError(_("The title is required."))

        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data["subtitle"]

        if not subtitle:
            raise forms.ValidationError(_("The subtitle is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', subtitle):
            raise forms.ValidationError(_("The subtitle contains unauthorized characters."))

        return subtitle

    def clean_content(self):
        content = self.cleaned_data["content"]
        clean_content=caption_optimizer(content)
        
        if not content:
            raise forms.ValidationError(_("The content is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', clean_content):
            raise forms.ValidationError(_("The content contains unauthorized characters."))

        return content
    
    def clean_media(self):
        image = self.cleaned_data["media"]

        if not image:
            raise forms.ValidationError(_("The image container cannot be empty."))

        image_format = imghdr.what(image)
        if image_format not in ['jpeg', 'png']:
            raise forms.ValidationError(_("The image format is not valid. Only JPEG and PNG files are allowed."))

        return image

    def clean_url(self):
        url = self.cleaned_data["url"]

        if not url:
            raise forms.ValidationError(_("The URL is required."))
        
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            raise forms.ValidationError("La URL no es válida.")
        return url

class RedirectContentForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ['media','title','subtitle','url',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
            
    def clean_title(self):
        title = self.cleaned_data["title"]

        if not title:
            raise forms.ValidationError(_("The title is required."))
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data["subtitle"]

        if not subtitle:
            raise forms.ValidationError(_("The subtitle is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', subtitle):
            raise forms.ValidationError(_("The subtitle contains unauthorized characters."))

        return subtitle

    def clean_content(self):
        content = self.cleaned_data["content"]
        clean_content=caption_optimizer(content)
        
        if not content:
            raise forms.ValidationError(_("The content is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', clean_content):
            raise forms.ValidationError(_("The content contains unauthorized characters."))

        return content
    
    def clean_media(self):
        image = self.cleaned_data["media"]

        if not image:
            raise forms.ValidationError(_("The image container cannot be empty."))

        image_format = imghdr.what(image)
        if image_format not in ['jpeg', 'png']:
            raise forms.ValidationError(_("The image format is not valid. Only JPEG and PNG files are allowed."))

        return image

    def clean_url(self):
        url = self.cleaned_data["url"]

        if not url:
            raise forms.ValidationError(_("The URL is required."))
        
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            raise forms.ValidationError("La URL no es válida.")
        return url

class StickerContentForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ['media','url']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
        
    def clean_media(self):
        image = self.cleaned_data["media"]

        if not image:
            raise forms.ValidationError(_("The image container cannot be empty."))

        image_format = imghdr.what(image)
        if image_format not in ['jpeg', 'png']:
            raise forms.ValidationError(_("The image format is not valid. Only JPEG and PNG files are allowed."))

        return image

    def clean_url(self):
        url = self.cleaned_data["url"]

        if not url:
            raise forms.ValidationError(_("The URL is required."))
        
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            raise forms.ValidationError("La URL no es válida.")
        return url
            
class GalleryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
                {'class': 'form-control'})
    class Meta:
        model = ImageGallery
        fields = ['image'] 

class BulletSimpleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False

    class Meta:
        model = DynamicBullets
        fields = ['bullet_title','content_bullet'] 

class ImageContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})

    class Meta:
        model = Content
        fields = ['media'] 

class FAQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            self.fields['status'].widget.attrs.update(
                {'class': 'custom-select custom-select-sm'})
            self.fields['legal'].widget.attrs.update(
                {'class': 'custom-select custom-select-sm'})
            
    class Meta:
        model = FAQ
        fields = '__all__'
        exclude = ('author','lang',)
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        if not title:
            raise forms.ValidationError(_("The title is required."))

        return title

class SetFaqForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False

    class Meta:
        model = SetFaq
        fields = '__all__'
        exclude = ('faq',)
    
    def clean_question(self):
        question = self.cleaned_data["question"]

        if not question:
            raise forms.ValidationError(_("The question is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', question):
            raise forms.ValidationError(_("The question contains unauthorized characters."))

        return question

    def clean_answer(self):
        answer = self.cleaned_data["answer"]
        clean_content=caption_optimizer(answer)

        if not answer:
            raise forms.ValidationError(_("The answer is required."))
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', clean_content):
            raise forms.ValidationError(_("The answer contains unauthorized characters."))

        return answer

class BlogForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ['status','category','title','subtitle','content','media','folder_doc',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
        self.fields['media'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['folder_doc'].widget.attrs.update(
            {'class': 'form-control'})
            
            
    def clean_title(self):
        title = self.cleaned_data["title"]

        if not title:
            raise forms.ValidationError(_("The title is required."))
        
        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', title):
            raise forms.ValidationError(_("The title contains unauthorized characters."))

        return title

    def clean_subtitle(self):
        subtitle = self.cleaned_data["subtitle"]

        if not subtitle:
            raise forms.ValidationError(_("The subtitle is required."))

        if not re.match(r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$', subtitle):
            raise forms.ValidationError(_("The subtitle contains unauthorized characters."))

        return subtitle

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError(_("The content is required."))
    
        message_formatted = caption_optimizer(content)
        print(message_formatted)
        regex = r"^[a-zA-Z0-9\s.,#-ñÑáéíóúÁÉÍÓÚ]*$"
        match = re.match(regex, message_formatted, re.DOTALL)
        if not match:
            raise forms.ValidationError(_("The content contains unauthorized characters."))
        
        return content
    
    def clean_media(self):
        image = self.cleaned_data["media"]

        if not image:
            raise forms.ValidationError(_("The image container cannot be empty."))

        image_format = imghdr.what(image)
        if image_format not in ['jpeg', 'png']:
            raise forms.ValidationError(_("The image format is not valid. Only JPEG and PNG files are allowed."))

        return image
    
    def clean_folder_doc(self):
        doc = self.cleaned_data["folder_doc"]
        if not doc:
            pass
        else:
            if not doc.name.endswith('.pdf'):
                raise forms.ValidationError("El archivo debe ser en formato PDF.")

        return doc

    def clean_url(self):
        url = self.cleaned_data["url"]

        if not url:
            raise forms.ValidationError(_("The URL is required."))
        
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            raise forms.ValidationError("La URL no es válida.")
        return url
    
#user
class DataEmailForm(forms.ModelForm):
    class Meta:
        model = DataEmail
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs.update(
            {'placeholder': _('Place Your Email')})
        
class CompanyForm(forms.ModelForm):
    class Meta: 
        model = Company
        fields = '__all__'
        exclude = ('owner','city_legal','lang','business')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
            field.required = True
            self.fields['logo'].widget.attrs.update(
                {'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        epattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(epattern, email):
            raise forms.ValidationError(_('Please enter a valid email.'))
        return email

    def clean_phone(self):
        phone=self.cleaned_data.get('phone')
        s = str(phone)
        clean_string = s.replace(" ", "").replace("-", "")
        pattern = r'^\+[\d\s]{10,12}$'
        if not re.match(pattern, clean_string):
            raise forms.ValidationError(_('Only this format is allowed (+123456789)'))
        else:
            clean_number = phonenumbers.parse(clean_string, None)
            if phonenumbers.is_possible_number(clean_number):
                return phone
            else:
                raise forms.ValidationError(_('This phonenumber is not valid'))
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        tpattern = r"^[a-zA-Z0-9\-/., ]*$" 
        if not re.match(tpattern, name):
            raise forms.ValidationError(_('Special characters are not allowed.'))
        return name

    def clean_web(self):
        web = self.cleaned_data.get('web')
        return web

    def clean_address(self):
        address = self.cleaned_data.get('address')
        message_formatted = caption_optimizer(address)

        if not address:
            raise forms.ValidationError(_("The content is required."))
        
        regex = r'^[a-zA-Z0-9\s!.,?;:"\'áéíóúÁÉÍÓÚñÑüÜ]+$'
        if not re.match(regex, message_formatted):
            raise forms.ValidationError(_('Special characters are not allowed.'))
        return address

class SocialMediaForm(forms.ModelForm):
    class Meta: 
        model = SocialLinks
        fields = '__all__'
        exclude = ('parent',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
    
class CommentsFormBlog(forms.ModelForm):
    class Meta: 
        model = Comments
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["post"].disabled = True
        self.fields["name"].disabled = True
        self.fields["email"].disabled = True
        self.fields["host"].disabled = True
        self.fields["message"].disabled = True
        
class UserForm(forms.ModelForm):
    class Meta:
        model = UserBase
        exclude = ('about','zip','image','password','last_login','is_staff')
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_profile'].queryset = City.objects.none()
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
        self.fields['cloud_id'].required = False
        
        if 'country_profile' in self.data:
            try:
                country_id = int(self.data.get('country_profile'))
                self.fields['city_profile'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            try:
                self.fields['city_profile'].queryset = self.instance.country_profile.city_set.all()
            except:
                self.fields['city_profile'].queryset = City.objects.none()
        
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
#linkzone
# class DynamicSecForm(forms.ModelForm):
#     class Meta:
#         model = Lobby
#         fields = '__all__'


class SiteNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].widget.attrs.update(
                {'class': 'form-control'})
    class Meta:
        model = Content
        fields = ['status', 'title', 'media', 'subtitle', 'content', 'url']

class FAQSiteForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        
#Email_Marketing
class NewsletterForm(forms.ModelForm):
    
    class Meta: 
        model = DataEmail
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email:
            raise ValidationError(_('Email is required.'))
        elif DataEmail.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already subscribed.'))
        elif not pattern.match(email):
            raise ValidationError(_('The email address is not valid.'))
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control required email bg-white border-0', 'placeholder': _('Place Email')})
        self.fields['email'].label=False
        
#orders 


# class CommentForm(forms.ModelForm):
#     class Meta: 
#         model = Comment
#         fields = ['user','status','comment','rate',]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["user"].disabled = True
#         self.fields["comment"].disabled = True
#         self.fields["rate"].disabled = True

#Stela Payments
class WalletForm(forms.ModelForm):
    class Meta: 
        model = Wallet
        exclude = ('user',)
        fields = '__all__'

#Post Facebook
class DateInput(forms.DateInput):
    input_type = 'date'

class FbPostForm(forms.ModelForm):

    class Meta:
        model=FacebookPostPage
        exclude = ('page' 'feed_id',)
        fields = '__all__'
        widgets = {
            'schedule': DateInput()
        }
           
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label=False
        self.fields["content"].required = False
        self.fields['content'].widget.attrs.update(
            {'onchange': 'submitTrigger()'})
        self.fields["schedule"].required = False
        self.fields["schedule"].label = False
        self.fields['schedule'].widget.attrs.update({'min': date.today() + timedelta(days=1), 'max': (date.today() + timedelta(days=180)).strftime('%Y-%m-%d')})
        
class FacebookMediaForm(forms.ModelForm):

    class Meta:
        model = FacebookPostMedia
        exclude = ('post',)
        fields = '__all__'

class FacebookEventsForm(forms.ModelForm):

    class Meta:
        model = FacebookPageEvent
        exclude = ('owner',)
        fields = '__all__'
        widgets = {
            'start_time': DateInput(),
            'end_time': DateInput(),

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = False
        self.fields['type'].label = False
        self.fields['category'].label = False
        self.fields['name'].label = False
        self.fields['start_time'].label = False
        self.fields['description'].label = False
        self.fields['description'].required = False
        self.fields['cover'].label = False
        self.fields['cover'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'vh-20'})
        self.fields['start_time'].widget.attrs.update({'min': date.today() + timedelta(days=1), 'max': (date.today() + timedelta(days=180)).strftime('%Y-%m-%d')})

class IGPostForm(forms.ModelForm):

    class Meta:
        model=IGPost
        exclude = ('parent',)
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = False
        self.fields['mediatype'].label = False
        self.fields['caption'].label = False
        self.fields['schedule'].label = False
        self.fields['status'].widget.attrs.update(
            {'class': 'custom-select custom-select-sm'})
        self.fields['mediatype'].widget.attrs.update(
            {'class': 'custom-select custom-select-sm'})

class IGMediaForm(forms.ModelForm):

    class Meta:
        model=IGMediaContent
        exclude = ('post',)
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover'].widget.attrs.update(
                {'class': 'form-control', 'accept': '.jpg'})
        self.fields['media'].widget.attrs.update(
                {'class': 'form-control', 'accept': '.mp4'})

class SendGridForm(forms.Form):
    email = forms.EmailField(label=_('To Email'))
    subject = forms.CharField(label=_('Subject'))
    client = forms.CharField(label=_('Client or Brand'))
    message = forms.CharField(widget=forms.Textarea, label=_('Report'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.label = False
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        epattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(epattern, email):
            raise forms.ValidationError(_('Please enter a valid email.'))
        return email

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        tpattern = r"^[a-zA-Z0-9\-/., ñÑáéíóúÁÉÍÓÚ]*$"
        if not re.match(tpattern, subject):
            raise forms.ValidationError(_('Special characters are not allowed.'))
        return subject

    def clean_client(self):
        client = self.cleaned_data.get('client')
        tpattern = r"^[a-zA-Z0-9\-/., ñÑáéíóúÁÉÍÓÚ]*$"
        if not re.match(tpattern, client):
            raise forms.ValidationError(_('Special characters are not allowed.'))
        return client

    def clean_message(self):
        message = self.cleaned_data.get('message')
        message_formatted = caption_optimizer(message)
        print(message_formatted)
        regex = r"^[a-zA-Z0-9\s.,#-ñÑáéíóúÁÉÍÓÚ]*$"
        match = re.match(regex, message_formatted, re.DOTALL)
        if not match:
            print('not validated')
            raise forms.ValidationError(_('Special characters are not allowed.'))
        return message

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['message', 'rate']

#siteapp Forms
class LiteraryWorkForm(forms.ModelForm):
    class Meta:
        model = LiteraryWork
        fields = ('title', 'author', 'publication_date', 'genre', 'synopsis')
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError(_("El title must be at least 5 characters."))
        return title

    def clean_publication_date(self):
        publication_date = self.cleaned_data['publication_date']
        if publication_date.year < 1800:
            raise forms.ValidationError(_("The pub date must be after 1800"))
        return publication_date

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file']

class BillFileForm(forms.ModelForm):
    class Meta:
        model = BillFile
        fields = ['title', 'pdf', 'comments']