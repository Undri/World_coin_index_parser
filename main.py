#!/usr/bin/env python3.4


def lr1():
    import urllib.request
    import urllib.parse
    # import requests
    from pyparsing import makeHTMLTags, SkipTo, withAttribute
    from prettytable import PrettyTable

    print("Parsing https://www.worldcoinindex.com/")
    url = 'https://www.worldcoinindex.com'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req)
    respData = str(resp.read())
    resp.close()
    tbody_Start, tbody_End = makeHTMLTags('tbody')
    tbody = tbody_Start + SkipTo(tbody_End)("body") + tbody_End
    tbody_string = ""
    for tokens, start, end in tbody.scanString(respData):
        tbody_string = tbody_string + tokens.body
    # print(tbody_string)

    # creating a list for bitcoin names
    btc = []
    # parsing bitcoin names
    h1_Start, h1_End = makeHTMLTags('h1')
    h1_body = h1_Start + SkipTo(h1_End)("body") + h1_End
    bitcoin_name = ""
    for tokens, start, end in h1_body.scanString(tbody_string):
        bitcoin_name = bitcoin_name + "\n" + tokens.body

    # getting rid of <span>
    span_start, span_end = makeHTMLTags("span")
    span_body = span_start + SkipTo(span_start | span_end)("body")
    for tokens, start, end in span_body.scanString(bitcoin_name):
        btc.append(tokens.body)

    # creating a list for bitcoin prices
    prices = []
    # parsing bitcoin prices
    price_start, price_end = makeHTMLTags('td')
    price_td = price_start.setParseAction(withAttribute(**{"class": "number pricekoers lastprice"}))
    price_body = price_td + SkipTo(price_start | price_end)("body")
    price_string = ""
    for tokens, start, end in price_body.scanString(respData):
        price_string = price_string + "\n" + tokens.body

    # getting rid of <span>
    span_class = span_start.setParseAction(withAttribute(**{"class": "span"}))
    span_body = span_class + SkipTo(span_class | span_end)("body")
    for tokens, start, end in span_body.scanString(price_string):
        prices.append(tokens.body)
    # print(prices)

    # generating PrettyTable
    t = PrettyTable()
    t.field_names = [" ", "Name", "Resent Price"]
    i = 0
    for x in btc:
        t.add_row([i + 1, x, prices[i]])
        i = i + 1
    t.align["Name"] = "c"
    t.align["Recent Price"] = "c"
    print(t)

    # saving data
    f = open('logs.txt', 'w')
    f.writelines(str(t))
    f.close()


print("\n\n PARSER")
lr1()


