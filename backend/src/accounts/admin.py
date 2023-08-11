from django.contrib import admin

from accounts.models import Account, AuthUser

admin.site.register(Account)
admin.site.register(AuthUser)
