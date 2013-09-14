from collections import defaultdict
from optparse import make_option
from django.core.management.base import BaseCommand
from main.models import Entity, FundingRound

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--run',
            action='store_true',
            dest='run',
            default=False,
            help='Run'),)

    def handle(self, *args, **options):
        err = self.stderr
        out = self.stdout
        if options['run']:
            run()

def companies_founded():
    for company in Entity.objects.filter(founded_year__gt=2007, is_company=True):
        print "%s#%s#%s#%s" % (company.permalink,company.name,company.founded_year, company.founded_month)

def company_funding():
    #Count how many companies received funding in a specific year
    years={}
    for funding_round in FundingRound.objects.filter(funded_year__gt=2002):
        if funding_round.investors.all().count()<=0:
            continue
        if funding_round.funded_year not in years:
            years[funding_round.funded_year] = {}
        try:
            company = funding_round.funding_rounds.all()[0]
            if company.is_company:
                years[funding_round.funded_year][company.permalink]=True
            else:
                print company.name
        except:
            pass
    for year,current_years_companies in years.items():
        total_companies = len(current_years_companies.keys())
        new_companies = 0
        repeat_companies = 0
        for company in current_years_companies.keys():
            company_funded_earlier = False
            for test_year in years.keys():
                if test_year >= year:
                    continue
                if company in years[test_year]:
                    company_funded_earlier = True
                    break
            if not company_funded_earlier:
                new_companies += 1
#        print "%s,%s,%s,%s" % (year, total_companies, "","")
        print "%s,%s,%s,%s" % (year, total_companies, total_companies - new_companies, new_companies)

def total_investments():
    years={}
    for funding_round in FundingRound.objects.filter(funded_year__gt=2007):
        if funding_round.investors.all().count()<=0:
            continue
        if funding_round.funded_year not in years:
            years[funding_round.funded_year] = {"companies":{},"total_amount":0}
        try:
            company = funding_round.funding_rounds.all()[0]
            if company.is_company:
                years[funding_round.funded_year]["companies"][company.permalink]=True
                years[funding_round.funded_year]["total_amount"] += funding_round.raised_amount
        except:
            pass
    for year in years.keys():
        print "%s,%s,%s" % (year, len(years[year]["companies"].keys()), years[year]["total_amount"])

def states():
    """
    states where new startups were launched
    """
    location = defaultdict(int)
    for company in Entity.objects.filter(founded_year=2012, is_company=True):
        for office in company.offices.all():
            key = "%s-%s" % (office.state_code, office.country_code)
            location[key] += 1
    for l in location.keys():
        print "%s,%s" % (l,location[l])

def num_investors():
    years={}
    for funding_round in FundingRound.objects.filter(funded_year__gt=2002):
        if funding_round.investors.all().count()<=0:
            continue
        if funding_round.funded_year not in years:
            years[funding_round.funded_year] = {"num_investors":0,"investors":{}}
        try:
            company = funding_round.funding_rounds.all()[0]
            if company.is_company:
                years[funding_round.funded_year]["num_investors"] += funding_round.investors.all().count()
                for investor in funding_round.investors.all():
                    years[funding_round.funded_year]["investors"][investor.permalink] = investor
        except:
            pass
    for year in years.keys():
        new_investors=0
        for investor in years[year]["investors"].keys():
            investor_funded_earlier=False
            for test_year in years.keys():
                if test_year >= year:
                    continue
                if investor in years[test_year]["investors"]:
                    investor_funded_earlier=True
                    break
            if not investor_funded_earlier:
                new_investors += 1
        print "%s,%s,%s,%s" % (year, years[year]["num_investors"],years[year]["num_investors"] - new_investors, new_investors)

def rounds():
    years={}
    for funding_round in FundingRound.objects.filter(funded_year__gt=2007):
        if funding_round.investors.all().count()<=0:
            continue
        if funding_round.funded_year not in years:
            years[funding_round.funded_year] = defaultdict(int)
        try:
            company = funding_round.funding_rounds.all()[0]
            if company.is_company:
                years[funding_round.funded_year][funding_round.round_code] += 1
        except:
            pass
    for year in years.keys():
        for round in years[year].keys():
            print "%s,%s,%s" % (year, round, years[year][round])

def category_code():
    years={}
    for funding_round in FundingRound.objects.filter(funded_year__gt=2007):
        if funding_round.investors.all().count()<=0:
            continue
        if funding_round.funded_year not in years:
            years[funding_round.funded_year] = defaultdict(float)
        try:
            company = funding_round.funding_rounds.all()[0]
            if company.is_company:
                years[funding_round.funded_year][company.category_code] += funding_round.raised_amount
        except:
            pass
    for year in years.keys():
        for category_code in years[year].keys():
            print "%s,%s,%s" % (year, category_code, years[year][category_code])

def find_companies():
    for e in Entity.objects.filter(is_company=True, total_money_raised__gt=40000000):
        is_CA = e.offices.filter(state_code='CA').count()
        if is_CA > 0:
            city = ""
            count = 1
            for office in e.offices.filter(state_code='CA'):
                city += office.city
                if count < is_CA:
                    city += ", "
                count+=1
        else:
            city = 'N/A'
        print "%s~%s~%s~%s~%s~%s~%s~%s" % (
            e.id,
            e.name,
            "http://www.crunchbase.com/company/"+e.permalink,
            e.founded_year,
            e.category_code,
            e.total_money_raised,
            is_CA,
            city
        )

def run():
#    companies_founded()
#    company_funding()
#    total_investments()
#    states()
#    num_investors()
#    rounds()
#    category_code()
    find_companies()