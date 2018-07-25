from login import InfrontConnect, socketconn, socket
import psycopg2 as pg
from operator import itemgetter


equity_markets = {
    'no': 18177,
    'au': 5460,
    'gr': 5030,
    'br': 7750,
    'mx': 7770,
    'es': 2012,
    'ro': 7800,
    'hu': 5000,
    'dk': 17665,
    'nl': 2009,
    'be': 2010,
    'pt': 2059,
    'fr': 2008,
    'de': 26,
    'is': 117,
    'tr': 5060,
    'za': 5070,
    'uk': 19,
    'it': 2047,
    'cz': 6380,
    'ch': 2057,
    'cn': 7970,
    'se': 17921,
    'at': 2139,
    'hr': 5710
    }

sector_group = {
    'agri': ['Food Products','Farming & Fishing', 'Food Products', 'Distillers & Vintners', 'Brewers'],
    'auto': ['Tires','Commercial Vehicles & Trucks','Trucking','Transportation Services','Auto Parts','Automobiles'],
    'bsc': ['Paper','Steel', 'Gold Mining', 'Industrial Machinery','Nonferrous Metals', 'Platinum & Precious Metals',
            'Diamonds & Gemstones','Specialty Chemicals', 'Forestry', 'Electrical Components & Equipment',
            'Gas Distribution', 'Electricity', 'Iron & Steel', 'Alternative Electricity', 'Coal', 'Commodity Chemicals',
            'Alternative Fuels', 'Industrial Suppliers', 'General Mining,Aluminum'],
    'cyc': ['Nondurable Household Products', 'Business Training & Employment Agencies', 'Specialty Retailers',
            'Clothing & Accessories', 'Electronic Office Equipment', 'Delivery Services', 'Travel & Tourism', 'Airlines',
            'Industrial Suppliers', 'Specialized Consumer Services', 'Heavy Construction', 'Restaurants & Bars',
            'Transportation Services', 'Containers & Packaging', 'Business Support Services'],
    'ene': ['Exploration & Production', 'Renewable Energy Equipment', 'Integrated Oil & Gas', 'Conventional Electricity',
            'Electrical Components & Equipment', 'Electricity','Alternative Electricity', 'Marine Transportation',
            'Coal','Alternative Fuels', 'Oil Equipment & Services'],
    'fcl': ['Specialty Finance', 'Banks,Consumer Finance', 'Financial Administration', 'Reinsurance', 'Mortgage Finance',
            'Property & Casualty Insurance', 'Property &Casualty Insurance', 'Asset Managers',
            'Equity Investment Instruments', 'Full Line Insurance', 'Life Insurance',
            'Nonequity Investment Instruments', 'Insurance Brokers', 'Investment Services'],
    'hcr': ['Medical Equipment', 'Biotechnology', 'Medical Supplies', 'Health Care Providers', 'Pharmaceuticals',
            'Drug Retailers'],
    'ment': ['Publishing', 'Media Agencies', 'Recreational Products', 'Gambling', 'Broadcasting & Entertainment',
             'Hotels', 'Recreational Services'],
    'ncy': ['Toys','Tobacco','Consumer Electronics','Footwear','Broadline Retailers','Nondurable Household Products',
            'Soft Drinks','Personal Products','Specialty Retailers','Clothing & Accessories','Delivery Services',
            'Transportation Services','Furnishings','Home Improvement Retailers','Food Retailers & Wholesalers',
            'Brewers','Durable Household Products','Apparel Retailers'],
    'recn': ['Diversified REITs','Speciality REITs','Real Estate Services','Home Construction','Mortgage REITs',
             'Hotel & Lodging REITs','Real Estate Holding & Development','Retail REITs','Building Materials & Fixtures',
             'Hotels','Residential REITs','Industrial & Office REITs'],
    'tec': ['Internet','Computer Hardware','Electronic Equipment','Biotechnology','Computer Services','Semiconductors',
            'Software'],
    'tel': ['Fixed Line Telecommunications','Mobile Telecommunications','Electrical Components & Equipment',
            'Telecommunications Equipment'],
    'uti': ['Railroads','Industrial Machinery','Water','Conventional Electricity','Electrical Components & Equipment',
            'Gas Distribution','Electricity','Alternative Electricity','Pipelines','Aerospace','Industrial Suppliers',
            'Heavy Construction','Multiutilities','Waste & Disposal Services']
}

# SQL querries for sectors and segments
class SectorQuerry:
    def __init__(self,dbname='infront', user='ihs3', password='ihs3', host = '10.234.10.30'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def create_connection(self):
        try:
            self.conn = pg.connect("dbname='" + self.dbname + "' user='" + self.user + "' password='" + self.password +
                                  "' host='" + self.host + "'")
            print("IHS connection: Success")
        except:
            print("Unable to connect to the database")

    def send_querry(self,querry_string):
        cursor = self.conn.cursor()
        cursor.execute(querry_string)
        out = cursor.fetchall()
        print('Querry: Instruments have been fetched')
        return out

#Generated the querry format to ask for the sector or segment of an instrument
def get_instrument_list(country_code,asset_class='eq'):
    if asset_class == "eq":
        querry = "select feednu, ticker, string_value from symbol_tags join symbol_map using(Feednu, symbolid)" + "where tag = 8599 and feednu = " + str(equity_markets[country_code])+ "and status = 0;"
        print("Querry generated for feed: " + str(equity_markets[country_code]))
    else:
        print("Asset type not supported")
    return querry

#Creates the list of instruments by sector
def sector_list(instrument_list, sectors):
    instrument_post = []
    for s in sectors:
        for i in instrument_list:
            if i[2] in sector_group[s]:
                var = i + (s,)
                instrument_post.append(var)
            else:
                pass
    return instrument_post

#Takes the tuples returned from the SQL querry, and transforms it to a dict format for JSON
def make_inst_list(instrument_list, sectors):
    instrument_post = sector_list(instrument_list, sectors)
    request = []
    for p in instrument_post:
        d = {'feed': p[0], 'ticker': p[1]}
        request.append(d)
    print("Instrument list generated. Ready to post.")
    return request

#Generates ranked lists
def sector_ranking(response, sector_list, sectors):
    struct = {}
    for s in sectors:
        struct[s] = []
        for i in sector_list:
            if i[3] == s:
                struct[s].append({'feed': i[0], 'ticker': i[1]})
            else:
                pass
    tickers = {}
    for s in sectors:
        tickers[s] = [r['ticker'] for r in struct[s]]

    rankdict = {}
    for s in sectors:
        rankdict[s] = []
        for d in response:
            if d['instrument']['ticker'] in tickers[s]:
                rankdict[s].append({'feed': d['instrument']['feed'],
                                    'ticker': d['instrument']['ticker'],
                                    'last': d['last'],
                                    'pct_change': d['pct_change']})
    rank = {}
    for s in rankdict:
        rank[s] = sorted(rankdict[s], key=itemgetter('pct_change'), reverse=True)

    return rank

#Class for generation of sector reports
class CountryOverview:
    def __init__(self, token, country_code, sectors):
        self.token = token
        self.country = country_code
        self.sectors = sectors

    def getSnapshot(self):
        querry = SectorQuerry()
        querry.create_connection()
        inst_list = querry.send_querry(get_instrument_list(self.country))
        md_get_snapshot_request = {
            "session_token": self.token,
            "md_get_snapshot_request": {
                "fields": ["LAST","PCT_CHANGE"],
                "instruments": make_inst_list(inst_list, self.sectors)
            }
        }
        print("Posting request to MWS. The list contains " + str(len(make_inst_list(inst_list, self.sectors))) + " instruments")
        response = socketconn(socket, md_get_snapshot_request)
        print("countryIndex: request successful")
        return response
    def countrySectors(self):
        md_get_chain_request = {
                "session_token": self.token,
                "md_get_chain_request": {
                    "chain": "OMXS30REAL",
                    "feed": 17921
                }
}
        response = socketconn(socket, md_get_chain_request)
        return response

# # create session
# test = InfrontConnect("alan.ipt","alan")
# token = test.login_keepAlive()
#
# #user specific report
# abc = CountryOverview(token, "no", ['tec','agri'])
# data = abc.getSnapshot()
#
# resp = data['md_get_snapshot_response']['instruments']
# # test
#
# t = SectorQuerry()
# t.create_connection()
# g = t.send_querry(get_instrument_list('no'))
# h = sector_list(g,['tec','agri'])
# f = make_inst_list(g, ['ene'])
#
# #creates a ranked lists based on percent change
# sectors = ['tec','agri']
# sector_ranking(resp,h,sectors)