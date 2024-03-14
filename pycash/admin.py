from pycash.models import *
from django.contrib import admin

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PaymentType)
admin.site.register(Tax)
admin.site.register(Expense)
admin.site.register(Debits)
admin.site.register(TokenUsage)
admin.site.register(Person)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(SyncRecord)
admin.site.register(Income)
admin.site.register(StatsData)
admin.site.register(CategoryStatsData)

class AuthTokenAdmin(admin.ModelAdmin):
    readonly_fields = ('token', 'token_key')
    
admin.site.register(AuthToken, AuthTokenAdmin)

from pycash.views import storeauthsetup
admin.site.register_view('storedtoken', storeauthsetup, 'Store Service Tokens', 'storedtoken')

#class StoredTokenForm(forms.ModelForm):
#
#    response = forms.CharField(required=False)
#    
#    def clean(self):
#        cleaned_data = super(StoredTokenForm, self).clean()
#        tkey = cleaned_data.get("token_key")
#        tsecret = cleaned_data.get("token_secret")
#        if tkey and tsecret:
#            cleaned_data['response'] = "lalala"
#            #raise forms.ValidationError("Did not send for 'help' in the subject despite CC'ing yourself.")
#        return cleaned_data
#    
#    class Meta:
#        model = StoredToken
#        exclude = ('token',)
#    
#class StoredTokenAdmin(admin.ModelAdmin):
#    form = StoredTokenForm
#    readonly_fields = ('updated',)
#    
#admin.site.register(StoredToken, StoredTokenAdmin)