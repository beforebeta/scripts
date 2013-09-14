from django.db import models
from django.utils import encoding
from picklefield.fields import PickledObjectField

class Tag(models.Model):
    name                    = models.CharField(max_length=255, blank=True, null=True)

class Image(models.Model):
    url                     = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    width                   = models.IntegerField(default=0)
    height                  = models.IntegerField(default=0)

class Relationship(models.Model):
    is_past                 = models.BooleanField(default=False)
    title                   = models.CharField(max_length=255, blank=True, null=True)
    person                  = models.ForeignKey('Entity', blank=True, null=True)

class FundingRound(models.Model):
    round_code              = models.CharField(max_length=255, blank=True, null=True)
    source_url              = models.CharField(max_length=255, blank=True, null=True)
    source_description      = models.CharField(max_length=255, blank=True, null=True)
    raised_amount           = models.FloatField(default=0)
    raised_currency_code    = models.CharField(max_length=255, blank=True, null=True)
    funded_year             = models.IntegerField(default=0)
    funded_month            = models.IntegerField(default=0)
    funded_day              = models.IntegerField(default=0)
    investors               = models.ManyToManyField('Entity', blank=True, null=True, related_name='investors')
    investments             = models.ManyToManyField('Entity', blank=True, null=True, related_name='entity_investments')

    def save(self, *args, **kwargs):
        if self.source_description:
            self.source_description = encoding.smart_str(self.source_description.encode('ascii','replace'))
        super(FundingRound, self).save(*args, **kwargs)


class Acquisition(models.Model):
    price_amount            = models.FloatField(default=0)
    price_currency_code     = models.CharField(max_length=255, blank=True, null=True)
    term_code               = models.CharField(max_length=255, blank=True, null=True)
    source_url              = models.CharField(max_length=255, blank=True, null=True)
    source_description      = models.CharField(max_length=255, blank=True, null=True)
    acquired_year           = models.IntegerField(default=0)
    acquired_month          = models.IntegerField(default=0)
    acquired_day            = models.IntegerField(default=0)
    company                 = models.ForeignKey('Entity', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.source_description:
            self.source_description = encoding.smart_str(self.source_description.encode('ascii','replace'))
        super(Acquisition, self).save(*args, **kwargs)

class Office(models.Model):
    description             = models.TextField()
    address1                = models.CharField(max_length=255, blank=True, null=True)
    address2                = models.CharField(max_length=255, blank=True, null=True)
    zip_code                = models.CharField(max_length=255, blank=True, null=True)
    city                    = models.CharField(max_length=255, blank=True, null=True)
    state_code              = models.CharField(max_length=255, blank=True, null=True)
    country_code            = models.CharField(max_length=255, blank=True, null=True)
    latitude                = models.CharField(max_length=255, blank=True, null=True)
    longitude               = models.CharField(max_length=255, blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.description:
            self.description = encoding.smart_str(self.description.encode('ascii','replace'))
        if self.address1:
            self.address1 = encoding.smart_str(self.address1.encode('ascii','replace'))
        if self.address2:
            self.address2 = encoding.smart_str(self.address2.encode('ascii','replace'))
        if self.zip_code:
            self.zip_code = encoding.smart_str(self.zip_code.encode('ascii','replace'))
        if self.city:
            self.city = encoding.smart_str(self.city.encode('ascii','replace'))
        if self.state_code:
            self.state_code = encoding.smart_str(self.state_code.encode('ascii','replace'))
        if self.country_code:
            self.country_code = encoding.smart_str(self.country_code.encode('ascii','replace'))
        super(Office, self).save(*args, **kwargs)

class IPO(models.Model):
    valuation_amount        = models.FloatField(default=0)
    valuation_currency_code = models.CharField(max_length=255, blank=True, null=True)
    pub_year                = models.IntegerField(default=0)
    pub_month               = models.IntegerField(default=0)
    pub_day                 = models.IntegerField(default=0)
    stock_symbol            = models.CharField(max_length=255, blank=True, null=True)

# Create your models here.
class Entity(models.Model):
    ##Entity General
    is_company              = models.BooleanField(default=False)
    is_financial_org        = models.BooleanField(default=False)
    is_person               = models.BooleanField(default=False)
    name                    = models.CharField(max_length=255, blank=True, null=True)
    first_name              = models.CharField(max_length=255, blank=True, null=True)
    last_name               = models.CharField(max_length=255, blank=True, null=True)
    permalink               = models.CharField(max_length=255, blank=True, null=True, unique=True, db_index=True)
    images                  = models.ManyToManyField(Image, blank=True)
    ## Company Specific
    crunchbase_url          = models.CharField(max_length=255, blank=True, null=True)
    homepage_url            = models.CharField(max_length=255, blank=True, null=True)
    blog_url                = models.CharField(max_length=255, blank=True, null=True)
    blog_feed_url           = models.CharField(max_length=255, blank=True, null=True)
    twitter_username        = models.CharField(max_length=255, blank=True, null=True)
    category_code           = models.CharField(max_length=255, blank=True, null=True)
    number_of_employees     = models.CharField(max_length=255, blank=True, null=True)
    founded_year            = models.IntegerField(default=0)
    founded_month           = models.IntegerField(default=0)
    founded_day             = models.IntegerField(default=0)
    deadpooled_year         = models.IntegerField(default=0)
    deadpooled_month        = models.IntegerField(default=0)
    deadpooled_day          = models.IntegerField(default=0)
    deadpooled_url          = models.CharField(max_length=255, blank=True, null=True)
    tags                    = models.ManyToManyField(Tag, blank=True)
    email_address           = models.CharField(max_length=255, blank=True, null=True)
    phone_number            = models.CharField(max_length=255, blank=True, null=True)
    description             = models.TextField(blank=True, null=True)
    created_at              = models.DateTimeField(blank=True, null=True)
    updated_at              = models.DateTimeField(blank=True, null=True)
    overview                = models.TextField(blank=True, null=True)
    relationships           = models.ManyToManyField(Relationship)
    competition             = models.ManyToManyField('Entity')
    total_money_raised      = models.FloatField(default=0)
    funding_rounds          = models.ManyToManyField(FundingRound,related_name='funding_rounds')
    investments             = models.ManyToManyField(FundingRound, related_name='funding_round_investments')
    acquisitions            = models.ManyToManyField(Acquisition)
    offices                 = models.ManyToManyField(Office)
    ipo                     = models.ForeignKey(IPO, blank=True, null=True)
    data                    = PickledObjectField()
    screenshots             = models.ManyToManyField(Image, related_name='screenshots')

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = encoding.smart_str(self.phone_number.encode('ascii','replace'))
        if self.name:
            self.name = encoding.smart_str(self.name.encode('ascii','replace'))
        if self.first_name:
            self.first_name = encoding.smart_str(self.first_name.encode('ascii','replace'))
        if self.last_name:
            self.last_name = encoding.smart_str(self.last_name.encode('ascii','replace'))
        super(Entity, self).save(*args, **kwargs)