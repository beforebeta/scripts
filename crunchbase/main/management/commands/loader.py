from optparse import make_option
from django.core.management.base import BaseCommand
import sys
import json
import time
from main import print_stack_trace
from main.models import *
from time import mktime
from datetime import datetime
from django.utils import encoding
import requests


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--load',
            action='store_true',
            dest='load',
            default=False,
            help='Load Data'),
        make_option('--companies',
            action='store_true',
            dest='companies',
            default=False,
            help='Load Data of Companies'),
    )

    def handle(self, *args, **options):
        err = self.stderr
        out = self.stdout
        if options['load']:
            load_from_file(sys.argv[3])
        elif options['companies']:
            load_companies()

def load_companies():
    companies = open("companies.js","r")
    companies = json.loads(companies.read())
    for company in companies:
        print company
        _company_js = open("files/%s.js" % company["permalink"],"w")
        _company_js.write(requests.get("http://api.crunchbase.com/v/1/company/%s.js?api_key=upkjyexdt2v9xxjesus7q2tr" % company["permalink"]).content)

def load_from_file(file_name):
    print "Loading Company Data"
    company_profiles = json.loads(open(file_name,"r").read())
    index = 0
    num = len(company_profiles.values())
    for company in company_profiles.values():
        print "%s/%s" % (index, num)
        load_company_profile(company)
        index += 1

def _get_dt(time_string):
    try:
        return datetime.fromtimestamp(mktime(time.strptime(time_string,"%a %b %d %H:%M:%S %Z %Y")))
    except:
        return None

def add_images_to_entity(images_dict, entity):
    #images
    try:
        entity.images.clear()
        for image in images_dict:
            url = image[1]
            if url.startswith("assets"):
                url = "http://www.crunchbase.com/"+url
            img,created = Image.objects.get_or_create(url=url)
            img.width = image[0][0]
            img.height = image[0][1]
            img.save()
            entity.images.add(img)
    except:
        print "Warning: no images for", entity.permalink

def transfer_field_values(fields, src_dict, target):
    for field in fields:
        try:
            if isinstance(field, tuple):
                key = field[0]
                val = field[1] if not src_dict[key] else src_dict[key]
            else:
                key = field
                val = src_dict[field]
            setattr(target, key, val)
        except:
            pass

def _get_person_obj(person_dict):
    person,created = Entity.objects.get_or_create(permalink=person_dict["permalink"])
    person.is_person = True
    person.first_name = encoding.smart_str(person_dict["first_name"].encode('ascii','replace'))
    person.last_name = encoding.smart_str(person_dict["last_name"].encode('ascii','replace'))
    person.name = "%s %s" % (person.first_name, person.last_name)
    person.save()
    try:
        add_images_to_entity(person_dict["image"]["available_sizes"], person)
    except:
        pass
    person.save()
    return person

def _get_company_or_fin_org(entity_dict, is_company=False, is_financial_org=False):
    entity,created = Entity.objects.get_or_create(permalink=entity_dict["permalink"])
    entity.is_company = is_company
    entity.is_financial_org = is_financial_org
    entity.name=entity_dict["name"]
    entity.save()
    try:
        add_images_to_entity(entity_dict["image"]["available_sizes"], entity)
    except:
        pass
    entity.save()
    return entity


def load_company_profile(company_profile):
    try:
        print company_profile["permalink"]
        entity,created = Entity.objects.get_or_create(permalink=company_profile["permalink"])
        fields= ["name","crunchbase_url", "homepage_url",
                      "blog_url", "blog_feed_url", "twitter_username",
                      "category_code", "number_of_employees",
                      ("founded_year",0), ("founded_month",0), ("founded_day",0),
                      ("deadpooled_year",0), ("deadpooled_month",0), ("deadpooled_day",0), "deadpooled_url",
                      "email_address", "phone_number"]
        transfer_field_values(fields, company_profile, entity)

        try:
            entity.description =  encoding.smart_str(company_profile["description"].encode('ascii','replace'))
        except:
            pass
        try:
            entity.overview =  encoding.smart_str(company_profile["overview"].encode('ascii','replace'))
        except:
            pass

        entity.is_company=True
        entity.data = company_profile

        entity.tags.clear()
        if company_profile["tag_list"]:
            for tag in company_profile["tag_list"].split(","):
                if len(tag)<=1:
                    continue
                t,created = Tag.objects.get_or_create(name=tag.lower())
                entity.tags.add(t)

        try:
            add_images_to_entity(company_profile["image"]["available_sizes"], entity)
        except:
            pass

        try:
            entity.relationships.all().delete()
            for reln in company_profile["relationships"]:
                if not "person" in reln:
                    print "Unrecognized relationship type", reln
                    continue
                relationship = Relationship()
                relationship.is_past = reln["is_past"]
                if relationship.is_past == None:
                    relationship.is_past = False
                relationship.title = reln["title"]
                relationship.person=_get_person_obj(reln["person"])
                relationship.save()
                entity.relationships.add(relationship)
        except:
            print_stack_trace()

        #Competition
        try:
            entity.competition.clear()
            for _competition in company_profile["competitions"]:
                competition = _competition["competitor"]
                competitor = _get_company_or_fin_org(competition,is_company=True)
                entity.competition.add(competitor)
        except:
            print_stack_trace()

        if company_profile["total_money_raised"]:
            try:
                if company_profile["total_money_raised"][0] == 'C':
                    company_profile["total_money_raised"] = company_profile["total_money_raised"][1:]
                if company_profile["total_money_raised"] == "$0":
                    entity.total_money_raised = 0
                else:
                    multiplier=1
                    if company_profile["total_money_raised"][-1].lower() == 'k':
                        multiplier=1000
                    elif company_profile["total_money_raised"][-1].lower() == 'm':
                        multiplier=1000000
                    elif company_profile["total_money_raised"][-1].lower() == 'b':
                        multiplier=1000000000
                    else:
                        print "--------------Unknown", company_profile["total_money_raised"]
                    entity.total_money_raised = float(company_profile["total_money_raised"][1:-1]) * multiplier
            except:
                print_stack_trace()

        if company_profile["funding_rounds"]:
            try:
                entity.funding_rounds.all().delete()
                for _funding_round in company_profile["funding_rounds"]:
                    round = FundingRound()
                    transfer_field_values([ "round_code", ("funded_year",0), ("funded_month",0), ("funded_day",0),
                                            "source_url", "source_description", ("raised_amount",0), "raised_currency_code"],
                        _funding_round, round)
                    round.save()
                    if _funding_round["investments"]:
                        for investment in _funding_round["investments"]:
                            if investment["company"]:
                                round.investors.add(_get_company_or_fin_org(investment["company"], is_company=True))
                            elif investment["financial_org"]:
                                round.investors.add(_get_company_or_fin_org(investment["financial_org"], is_financial_org=True))
                            elif investment["person"]:
                                round.investors.add(_get_person_obj(investment["person"]))
                            else:
                                print "Unknown investment", investment, entity.permalink
                    round.save()
                    entity.funding_rounds.add(round)
            except:
                print_stack_trace()

        if company_profile["investments"]:
            try:
                entity.investments.all().delete()
                for __investment in company_profile["investments"]:
                    _investment = __investment["funding_round"]
                    round = FundingRound()
                    transfer_field_values([ "round_code", ("funded_year",0), ("funded_month",0), ("funded_day",0),
                                            "source_url", "source_description", ("raised_amount",0), "raised_currency_code"],
                        _investment, round)
                    round.save()
                    if _investment["company"]:
                        round.investments.add(_get_company_or_fin_org(_investment["company"], is_company=True))
                    else:
                        print "Unknown funding round", _investment, entity.permalink
                    round.save()
                    entity.investments.add(round)
            except:
                print_stack_trace()

        if company_profile["acquisitions"]:
            try:
                entity.acquisitions.all().delete()
                for _acquisition in company_profile["acquisitions"]:
                    acquisition = Acquisition()
                    transfer_field_values([ ("price_amount",0), "price_currency_code", "term_code", "source_url",
                                            "source_description", ("acquired_year",0), ("acquired_month",0), ("acquired_day",0)],
                        _acquisition, acquisition)
                    acquisition.save()
                    if _acquisition["company"]:
                        acquisition.company = _get_company_or_fin_org(_acquisition["company"], is_company=True)
                    acquisition.save()
                    entity.acquisitions.add(acquisition)
            except:
                print_stack_trace()

        if company_profile["offices"]:
            entity.offices.all().delete()
            for _office in company_profile["offices"]:
                office = Office()
                transfer_field_values([ "address1", "address2", "zip_code", "city",
                                        "state_code", "country_code","latitude","longitude"],
                    _office, office)
                office.save()
                entity.offices.add(office)

        if company_profile["ipo"]:
            if entity.ipo:
                entity.ipo.delete()
                entity.ipo=None
                ipo = IPO()
                transfer_field_values([ "valuation_amount", "valuation_currency_code",
                                        ("pub_year",0), ("pub_month",0),("pub_day",0), "stock_symbol"],
                    company_profile["ipo"], ipo)
                ipo.save()
                entity.ipo=ipo

        try:
            add_images_to_entity(company_profile["screenshots"]["available_sizes"], entity)
        except:
            pass

#        entity.created_at = _get_dt(company_profile["created_at"])
#        entity.updated_at = _get_dt(company_profile["updated_at"])
        entity.save()
    except:
        print_stack_trace()

