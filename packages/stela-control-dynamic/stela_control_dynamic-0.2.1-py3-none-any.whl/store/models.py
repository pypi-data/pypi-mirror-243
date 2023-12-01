

# class Product(models.Model):
#     STATUS = (
#         ('Active', 'Active'),
#         ('Inactive', 'Inactive'),
#     )
#     title = models.CharField(verbose_name=_("Title"), help_text=_("Required"), max_length=255)
#     description = RichTextField(verbose_name=_("Description"), help_text=_("No Required"), blank=True)
#     image = models.ImageField(verbose_name=_("Image"), upload_to='images/') 
#     slug = models.SlugField(max_length=255, help_text=_("Required"))
#     status = models.CharField(max_length=10, choices=STATUS)
#     is_active = models.BooleanField(verbose_name=_("Product visibility"), help_text=_("Change product visibility"), default=True)
#     top_service = models.BooleanField(verbose_name=_("Costumer Choice"), help_text=_("Costumer Choice"), default=False)
#     new_service = models.BooleanField(verbose_name=_("New Service"), help_text=_("New Service"), default=False)
#     created_at = models.DateTimeField(_("Created"), auto_now_add=True, editable=False) 
#     updated_at = models.DateTimeField(_("Created at"), auto_now=True)

#     class Meta:
#         verbose_name = _("Product")
#         verbose_name_plural = _("Products")
    
#     def __str__(self):
#         return self.title

#     def image_tag(self):
#         if self.image.url is not None:
#             return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
#         else:
#             return ""

# #ORDERS
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_users',)
#     email = models.EmailField(null=True)
#     full_name = models.CharField(max_length=50, null=True)
#     address = models.CharField(max_length=250, null=True)
#     phone = models.CharField(max_length=13, null=True)
#     zipcode = models.CharField(max_length=20, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     appointment_date = models.DateField(null=True)
#     key_validator = models.CharField(max_length=200)
#     transaction_id = models.CharField(max_length=200, null=True)
#     stripe_order = models.CharField(max_length=200, null=True)
#     payment_option = models.CharField(max_length=200, blank=True, null=True)
#     subtotal = models.DecimalField(max_digits=7, decimal_places=2, null=True)
#     taxes = models.DecimalField(max_digits=7, decimal_places=2, null=True)
#     profit = models.DecimalField(max_digits=7, decimal_places=2, null=True)
#     payment_fee = models.DecimalField(max_digits=7, decimal_places=2, null=True)
#     total_paid = models.DecimalField(max_digits=7, decimal_places=2, null=True)
#     order_status = models.BooleanField(default=False, verbose_name=('Confirm'))
#     billing_status = models.BooleanField(default=False, verbose_name=('Payment'))
    
#     class Meta:
#         ordering = ('-created',)

#     def __str__(self):
#         return str(self.created)

#     def averageview(self):
#         reviews = Comment.objects.filter(order=self).aggregate(average=Avg('rate'))
#         avg = 0
#         if reviews["average"] is not None:
#             avg=float(reviews["average"])
#         return avg

# class PaypalClient(models.Model):
#       def __init__(self):
#         self.client_id = "AfA3d0-CCazeqNdk2AF_SSVdTLp0Eirwt-ku1rJsf-PcQMct4y3SCoeGyfYDj-nNI50v8EVtjr8OZ4q3"
#         self.client_secret = "EAhV7gKAbyoFjnN-Lw_40nbyV1xdei2yJHqRXUp-Mc6yA0j5fJNUfROtEx_Cz0oL_tvSdxxyeNO4DdaB"
#         self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
#         self.client = PayPalHttpClient(self.environment)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     service = models.ForeignKey(Product, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.created)

# class Comment(models.Model):
#    STATUS = (
#         ('New', 'New'),
#         ('True', 'True'),
#         ('False', 'False'),
#     )
#    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments')
#    product = models.ForeignKey(Product, on_delete=models.CASCADE)
#    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#    comment = models.TextField(max_length=250, blank=True)
#    rate = models.IntegerField(default=1)
#    ip = models.CharField(max_length=20, blank=True)
#    status = models.CharField(max_length=10, choices=STATUS, default='New', verbose_name="Change Status")
#    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)  
#    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

#    def __str__(self):
#        return self.created_at
   
# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment', 'rate']