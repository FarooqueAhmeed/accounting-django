from django.contrib import admin
from receipts.models import *


admin.site.register(CaptureReceipt)
admin.site.register(CaptureRecurringReceipt)