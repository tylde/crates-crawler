LOCAL_API = 'http://localhost:27777/api'
STEAM_API = 'http://steamcommunity.com'

CRATE_SUFFIX = {
    'ID_SUFFIX': '_CRATE_ID',
    'NAME_SUFFIX': '_CRATE_NAME',
    'SHORT_NAME_SUFFIX': '_CRATE_SHORT_NAME',
    'HISTOGRAM_ID_SUFFIX': '_ITEM_ORDERS_HISTOGRAM_ID',
    'PRICE_OVERVIEW_SUFFIX': '_PRICE_OVERVIEW_NAME'
}

SUMMARY_REGEX = "(?<=<span class=\"market_commodity_orders_header_promote\">)[0-9]+(?=</span>)"
