import requests
import json
from datetime import datetime

# Define the request URL
url = "https://csekhvms53-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.20.0)%3B%20Browser%3B%20JS%20Helper%20(3.14.0)%3B%20react%20(18.2.0)%3B%20react-instantsearch%20(6.40.4)&search_origin=companies_search_client"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "3024",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "csekhvms53-dsn.algolia.net",
    "Origin": "https://www.welcometothejungle.com",
    "Referer": "https://www.welcometothejungle.com/",
    "Sec-CH-UA": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-algolia-api-key": "4bd8f6215d0cc52b26430765769e65a0",
    "x-algolia-application-id": "CSEKHVMS53"
}

def fetch_companies(page):
    payload = {
        "requests": [
            {
                "indexName": "wk_cms_organizations_production",
                "params": (
                    "analyticsTags=page:companies_index,language:en"
                    "&aroundPrecision=20000"
                    "&attributesToHighlight=name"
                    "&attributesToRetrieve=cover_image.small.url,descriptions,featured_image.url,jobs_count,logo.large.url,logo.url,name,objectID,offices,profile_type,published_at,reference,sectors,slug,website,cover_image.en.small.url,size.en,accepts_spontaneous_application"
                    "&clickAnalytics=true"
                    "&facetFilters=[['languages:en']]"
                    "&facets=labels,languages,offices.country_code,offices.district,offices.location,offices.state,online,sectors.parent.en,sectors_name.en.Advertising / Marketing / Agency,sectors_name.en.Architecture,sectors_name.en.Banking / Insurance / Finance,sectors_name.en.Consulting / Audit,sectors_name.en.Corporate Services,sectors_name.en.Culture / Media / Entertainment,sectors_name.en.Distribution,sectors_name.en.Education / Training / Recruitment,sectors_name.en.Engineering,sectors_name.en.Fashion / Luxury / Beauty / Lifestyle,sectors_name.en.Food and Beverage,sectors_name.en.Health / Social / Environment,sectors_name.en.Hotel / Tourism / Leisure,sectors_name.en.Industry,sectors_name.en.Legal / Law,sectors_name.en.Mobility / Transport,sectors_name.en.Nonprofit / Association,sectors_name.en.Public Administration,sectors_name.en.Real Estate,sectors_name.en.Tech,size.en"
                    "&filters=website.reference:wttj_fr"
                    "&highlightPostTag=</ais-highlight-0000000000>"
                    "&highlightPreTag=<ais-highlight-0000000000>"
                    "&hitsPerPage=30"
                    "&maxValuesPerFacet=999"
                    f"&page={page}"
                    "&query="
                    "&tagFilters="
                    "&userToken=86028995-2a08-43dd-940c-fe39a5713f50"
                )
            },
            {
                "indexName": "wk_cms_organizations_production",
                "params": (
                    "analytics=false"
                    "&analyticsTags=page:companies_index,language:en"
                    "&aroundPrecision=20000"
                    "&attributesToHighlight=name"
                    "&attributesToRetrieve=cover_image.small.url,descriptions,featured_image.url,jobs_count,logo.large.url,logo.url,name,objectID,offices,profile_type,published_at,reference,sectors,slug,website,cover_image.en.small.url,size.en,accepts_spontaneous_application"
                    "&clickAnalytics=false"
                    "&facets=languages"
                    "&filters=website.reference:wttj_fr"
                    "&highlightPostTag=</ais-highlight-0000000000>"
                    "&highlightPreTag=<ais-highlight-0000000000>"
                    "&hitsPerPage=0"
                    "&maxValuesPerFacet=999"
                    f"&page={page}"
                    "&query="
                    "&userToken=86028995-2a08-43dd-940c-fe39a5713f50"
                )
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

# Main Logic
all_companies = []
page = 0
total_hits = 1  # Start with a non-zero value

while page * 30 < total_hits:
    print(f"Fetching page {page}...")
    response = fetch_companies(page)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            hits = data["results"][0]["hits"]
            total_hits = data["results"][0]["nbHits"]
            all_companies.extend(hits)
            print(f"Fetched page {page}, companies: {len(hits)}, total: {total_hits}")
            page += 1
        else:
            print("No results in response.")
            break
    else:
        print(f"HTTP Error {response.status_code}: {response.text}")
        break

# Save results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"companies_{timestamp}.json"
with open(filename, "w", encoding="utf-8") as file:
    json.dump(all_companies, file, indent=4, ensure_ascii=False)

print(f"Saved {len(all_companies)} companies to {filename}")