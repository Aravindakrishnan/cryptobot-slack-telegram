def get_chart_id(key):
    chart_lookup = {
    '1d' : 'react-tabs-0',
    '7d' : 'react-tabs-2',
    '1m' : 'react-tabs-4',
    '3m' : 'react-tabs-6',
    '1y' : 'react-tabs-8',
    'ytd' : 'react-tabs-10',
    'all' : 'react-tabs-12',
    }
    if key in chart_lookup :
        return chart_lookup[key]
    return {}

def fullscreen():
    return "//*[@id='__next']/div/div/div[2]/div/div[3]/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/button"