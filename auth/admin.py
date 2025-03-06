from django.contrib import admin
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

admin.site.register(BlacklistedToken)
admin.site.register(OutstandingToken)
