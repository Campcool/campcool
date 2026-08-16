import dns.resolver

for qt in ['NS', 'CNAME', 'A']:
    try:
        ans = dns.resolver.resolve('campcool.tw', qt)
        print(qt, [str(r) for r in ans])
    except Exception as e:
        print(qt, 'ERR:', e)
