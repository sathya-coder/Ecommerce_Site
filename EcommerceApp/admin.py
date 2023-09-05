from django.contrib import admin
from EcommerceApp.models.User import *
from EcommerceApp.models.Products import *

admin.site.register(Register)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Coupun)
admin.site.register(UsedCoupuns)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(PasswordResetToken)
