from django.db import models
from django.contrib.auth.models import User
from pycash.services.ModelUtils import capFirst
from django.conf import settings
    
class StoredToken(models.Model):
    token_key = models.CharField(max_length=255, db_index=True)
    token_secret = models.CharField(max_length=255, db_index=True)
    token = models.TextField()
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
 
    class Meta:
        get_latest_by = "updated"
        
class AuthToken(models.Model):
    token = models.CharField(max_length=128, primary_key=True)
    token_key = models.CharField(max_length=5)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, related_name="auth_token")
 
    def __unicode__(self):
        return u'%s - %s - %s' % (self.user, self.token, self.token_key)  
       
    def make_token(self):
        from django.utils.hashcompat import sha_constructor
        from random import choice
        import time
        allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        number_chars = '123456789'
        self.token = sha_constructor(str(time.time()) + ''.join([choice(allowed_chars) for i in range(10)])).hexdigest() 
        self.token_key = ''.join([choice(number_chars) for i in range(5)])
               
    def save(self, **args):
        if not self.pk:
            self.make_token()
        models.Model.save(self, **args)
        
    class Meta:
        ordering = ['created']
        get_latest_by = "created"
            
class TokenUsage(models.Model):
    token = models.ForeignKey(AuthToken)
    ip = models.CharField(max_length=15, db_index=True)
    access = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s - %s - %s' % (self.token.user, self.ip, self.access)  

    class Meta:
        get_latest_by = "access"
        
class Income(models.Model):
    period = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    
    def __unicode__(self):
        return u"%s" % self.period  

    class Meta:
        db_table = "income"
        verbose_name_plural = u'Incomes'
            
class PaymentType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def save(self):
        self.name = capFirst(self.name)
        super(PaymentType, self).save()
        
    def __unicode__(self):
        return u"(%s) %s" % (self.pk, self.name)
      
    class Meta:
        db_table = "payment_type"
        verbose_name_plural = u'Payment Types'
        
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def save(self):
        self.name = capFirst(self.name)
        super(Category, self).save()
        
    def __unicode__(self):
        return u"(%s) %s" % (self.pk, self.name)
        
    class Meta:
        db_table = "category"
        verbose_name_plural = u'Categories'
        
class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", db_column="category_id")

    def save(self):
        self.name = capFirst(self.name)
        super(SubCategory, self).save()
            
    def __unicode__(self):
        return "%s - %s" % (self.name, self.category.name)  
    class Meta:
        db_table = "sub_category"
        verbose_name_plural = u'Sub Categories'
            
class Tax(models.Model):
    paymentType = models.ForeignKey(PaymentType,db_column="payment_type_id")
    subCategory = models.ForeignKey(SubCategory,db_column="sub_category_id")
    service = models.CharField(max_length=200, blank=False, unique=True)
    account = models.CharField(max_length=50, blank=True)
    expire = models.DateField(db_index=True,)
    nextExpire = models.DateField(null=True,db_column="next_expire")
    lastPay = models.DateField(null=True,db_column="last_pay")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    gcalId = models.CharField(max_length=50, blank=True, db_column="gcal_id")
    updated = models.BooleanField(default=False)
    
    def save(self):
        self.name = capFirst(self.service)
        super(Tax, self).save()
            
    def __unicode__(self):
        return self.service
    
    class Meta:
        db_table = "tax"
        verbose_name_plural =u'Taxes'
        
class Expense(models.Model):
    subCategory = models.ForeignKey(SubCategory, db_column="sub_category_id")
    paymentType = models.ForeignKey(PaymentType, db_column="payment_type_id")
    date = models.DateField(db_index=True)
    text = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    def save(self, **kwargs):
        self.name = capFirst(self.text)
        super(Expense, self).save(kwargs)
        
    def __unicode__(self):
        return "(%s) %s - %s" % (self.date, self.text, self.subCategory.name)

    class Meta:
        db_table = "expense"
        verbose_name_plural = u'Expenses'
        
class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def save(self):
        self.name = capFirst(self.name)
        super(Person, self).save()
            
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = "person"
        
class LoanManager(models.Manager):
    
    def active(self):
        return self.filter(remain__gt=0)
    
    def fullpaid(self):
        return self.filter(remain=0)
    
class Loan(models.Model):
    person = models.ForeignKey(Person, db_column="person_id", related_name="loans")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateField(db_index=True)
    reason = models.CharField(max_length=255)
    instalments = models.IntegerField()
    remain = models.DecimalField(max_digits=19, decimal_places=2, db_index=True)
    
    objects = LoanManager()
    
    def save(self):
        self.name = capFirst(self.reason)
        super(Loan, self).save()
            
    def __unicode__(self):
        return "(%s) %s - %s" % (self.reason, self.amount, self.person.name)
    
    class Meta:
        db_table = "loan"
        
class Payment(models.Model):
    loan = models.ForeignKey(Loan, db_column="loan_id")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateField(db_index=True)
    
    def __unicode__(self):
        return "(%s) %s %s" % (self.loan.reason, self.amount, self.date)
    
    class Meta:
        db_table = "payment"
        ordering = ("-date",)
        
class Card(models.Model):
    name = models.CharField(max_length=50, unique=True)
    paymentType = models.ForeignKey(PaymentType, db_column="paymentType_id") 
    
    class Meta:
        db_table = "card"
        
class CardDates(models.Model):
    closeDate = models.DateField()
    expireDate = models.DateField()
    card = models.ForeignKey(Card, db_column="card_id")
    
    class Meta:
        db_table = "card_dates"
   
class CardData(models.Model):
    date = models.DateField()
    shop = models.CharField(max_length=100)
    instalments = models.IntegerField()
    total = models.DecimalField(max_digits=19, decimal_places=2)
    own = models.BooleanField()
    card = models.ForeignKey(Card, db_column="card_id")
    
    class Meta:
        db_table = "card_data"
         
class CardPayment(models.Model):
    minimum = models.DecimalField(max_digits=19, decimal_places=2)
    total = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.ForeignKey(CardDates, db_column="card_date_id")
    tax = models.ForeignKey(Tax, db_column="tax_id")
    
    class Meta:
        db_table = "card_payment"

class Debits(models.Model):
    day = models.IntegerField()
    subCategory = models.ForeignKey(SubCategory, db_column="sub_category_id")
    paymentType = models.ForeignKey(PaymentType, db_column="payment_type_id")
    text = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    since = models.DateField()
    last = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.text
        
    class Meta:
        db_table = "debits"
        verbose_name_plural = u'Debits'

class StatsData(models.Model):
    month = models.IntegerField(primary_key=True)
    expenses = models.DecimalField(max_digits=19, decimal_places=2)
    incomes = models.DecimalField(max_digits=19, decimal_places=2)
    
    def __unicode__(self):
        return "%s - E: %s - I: %s" % (self.display_month, self.expenses, self.incomes)
        
    @property
    def display_month(self):
        return u"%s-%s" % (str(self.month)[:4], str(self.month)[-2:])
    
    class Meta:
        db_table = "statsdata"
        verbose_name_plural = u'Stats'
        ordering = ("-month",)
        get_latest_by = "month"

class CategoryStatsData(models.Model):
    month = models.IntegerField(db_index=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    category = models.ForeignKey(Category)
    
    def __unicode__(self):
        return "%s - A: %s - Ca: %s" % (self.display_month, self.amount, self.category.name)
        
    @property
    def display_month(self):
        return u"%s-%s" % (str(self.month)[:4], str(self.month)[-2:])
    
    class Meta:
        db_table = "categorystatsdata"
        verbose_name_plural = u'Category Stats'
        ordering = ("-month", "category")
        get_latest_by = "month"
                
class SyncRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    record = models.TextField()
    operation = models.CharField(max_length=3)
    
    def __unicode__(self):
        return "(%s) %s" % (self.created, self.operation)
        
    class Meta:
        db_table = "syncrecord"
        verbose_name_plural = u'SyncRecords'
        ordering = ("created",)
    
record_sync_list = (Person, Income, PaymentType, Category, SubCategory, Tax, Expense, Loan, Payment)

def object_update_callbak(sender, instance, created, **kwargs):
    from django.core import serializers
    value = serializers.serialize("json",[instance])
    SyncRecord(record=value, operation= 'ADD' if created else 'UDP').save()
        
def object_delete_callbak(sender, instance, **kwargs):
    from django.utils.encoding import smart_unicode    
    SyncRecord(record='[{"pk": %(pk)s, "model": "%(model)s"}]' % {"model" : smart_unicode(instance._meta), "pk" : smart_unicode(instance._get_pk_val(), strings_only=True)}, operation='DEL').save()
    
def enable_sync():
    if getattr(settings, 'ENABLE_RECORD', False):
        from django.db.models.signals import post_save, post_delete
        for sender in record_sync_list:
            post_save.connect(object_update_callbak, sender)
            post_delete.connect(object_delete_callbak, sender)
            
def disable_sync():
    if getattr(settings, 'ENABLE_RECORD', False):
        from django.db.models.signals import post_save, post_delete
        for sender in record_sync_list:
            post_save.disconnect(object_update_callbak, sender)
            post_delete.disconnect(object_delete_callbak, sender)
    
enable_sync() 
