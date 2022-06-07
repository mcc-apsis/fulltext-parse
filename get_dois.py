#!/usr/bin/env python3

import pandas as pd
import requests

df = pd.read_csv('data/documents.csv', skiprows=1)
df = df[(df['docproject__relevant']=="Yes (1)") & (pd.notna(df['wosarticle__di']))].reset_index(drop=True)
df['redirect_url'] = None

header ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
for i, row in df.iterrows():
    url = row['wosarticle__di']
    with requests.Session() as s:
        r = s.get(url, headers=header, verify=False)
        if r.status_code==503:
            print(f"{url} returns a service unavailable error")
            continue
        elif r.status_code >= 500:
            print(f"{url} returns a {r.status_code} error")
            continue
        elif r.status_code >= 400:
            print(f"{url} returns a {r.status_code} error")
            continue   
            
        if "mdpi" in r.url:
            r = s.get(r.url+"/htm", verify=False)
        fname = url.split('org/')[-1].replace('/','__').replace('.','_')
        with open(f"fulltexts/{fname}.html","w") as f:
            f.write(r.text)
            
        df.loc[i,"redirect_url"] = r.url
        
df.to_csv('data/documents_parsed.csv',index=False)