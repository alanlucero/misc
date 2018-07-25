from pgquerry import SectorQuerry

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
def get_instrument_list(country_code,asset_class='eq'):
    if asset_class == "eq":
        querry = "select feednu, ticker, string_value from symbol_tags join symbol_map using(Feednu, symbolid)" + "where tag = 8599 and feednu = " + str(equity_markets[country_code])+ "and status = 0;"
        print("Querry generated for feed: " + str(equity_markets[country_code]))
    else:
        print("Asset type not supported")
    return querry

def make_inst_list(instrument_list):
    instrument_post = []
    for i in instrument_list:
        d = {'feed': i[0], 'ticker': i[1]}
        instrument_post.append(d)
    return instrument_post


