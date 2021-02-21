from django.contrib import admin
from .models import Ledger, LedgerItem

class LedgerAdmin(admin.ModelAdmin):
    pass

class LedgerSharedUsersAdmin(admin.ModelAdmin):
    pass

class LedgerItemAdmin(admin.ModelAdmin):
    pass

# Register your models here
admin.site.register(Ledger, LedgerAdmin)
admin.site.register(LedgerItem, LedgerItemAdmin)
