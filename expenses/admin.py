from django.contrib import admin
from .models import Group, Expense, ExpenseSplit, GroupMembership

admin.site.register(Group)
admin.site.register(Expense)
admin.site.register(ExpenseSplit)
admin.site.register(GroupMembership)