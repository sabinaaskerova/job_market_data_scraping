import requests
from bs4 import BeautifulSoup
from vars import *

# Define the login URL and the scraping URL
login_url = "https://www.upwork.com/ab/account-security/login"
scraping_url = "https://www.upwork.com/api/graphql/v1?alias=mostRecentJobsFeed"
session = requests.Session()

# Get the login page to extract the CSRF token
login_page_response = session.get(login_url)

# Parse the login page HTML to find the CSRF token
soup = BeautifulSoup(login_page_response.text, 'html.parser')
# csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
csrf_token = '94ce4e28077fd9f1c1eb4341b02475ad' # this doesn't work because token is dynamic

# Define the headers for the login request
login_headers = {
    "authority": "www.upwork.com",
    "method": "POST",
    "path": "/ab/account-security/login",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "content-length": "7106",
    "content-type": "application/json",
    "cookie": "G_AUTHUSER_H=0; AccountSecurity_cat=ab89c15e.oauth2v2_1f67c3f0adf57333b9799c171e909fd6; visitor_id=79.134.37.72.1724497328760000; spt=e100e574-e2f6-4038-acaa-c0b914db26a2; G_ENABLED_IDPS=google; _tt_enable_cookie=1; _ttp=cFIJsNm-_Kip_mwIl4-Daqg6pze; _cq_duid=1.1724497332.DDo3OenIcvrth7nm; __pdst=e847e94d94ad480b9ae21e74df66c177; IR_PI=522e6f7d-6208-11ef-9793-e7ef868ca4c3%7C1724497334653; device_view=full; OptanonAlertBoxClosed=2024-11-08T07:38:06.710Z; country_code=FR; cookie_prefix=; cookie_domain=.upwork.com; __cflb=02DiuEXPXZVk436fJfSVuuwDqLqkhavJbsr5LLHay1sLo; c1551dbbsb=oauth2v2_611f1aae638fb39cc1d817f1ed10093b; _cq_suid=1.1732385267.C77QLhewoyUs634N; FindWorkHome:hasInterviewsOrOffers=1; f2ea0346sb=oauth2v2_32ad9d039be1ef336f9e005def660b00; UniversalSearchNuxt_vt=oauth2v2_eab54d457d5a556d4c320e6f816266dc; _cfuvid=IWiyshjIOGhJ577rrjGBktQVgw86yjHB5L9bTzb2pcA-1732388558621-0.0.1.1-604800000; _upw_ses.5831=*; _ga=GA1.2.756219045.1724497334; _gid=GA1.2.1120544425.1732393344; user_oauth2_slave_access_token=73dda274.oauth2v2_a8ced74d1fe904bb8413e7742b23493e:1860418750955816703.oauth2v2_f6f4133f686a3de437ff9a23cec01558; visitor_signup_gql_token=oauth2v2_b8b714b08b79b8d15cabdadb40175caa; 55c3fb0fsb=oauth2v2_6b9445dba1a2977c5032588317c236e6; ftr_ncd=6; recognized=sabinaaskerova; company_last_accessed=d24669442; 22be2d03sb=oauth2v2_87f57364812ecd7c2b6e7064a3a7c3db; 3bd03668sb=oauth2v2_844af99b1a73ce81f3359dc0a6e600a4; 20e34b0asb=oauth2v2_3ece7560e74607bbae89853b3fcfed7e; __cf_bm=3B.bYwU1ex4EFsXl6e4_fcd_OEHbmMsU6uNhKWki2XI-1732395164-1.0.1.1-FKhPPdIbWBtYV9zH8JrT5ZnZapOqnWnNBCY6vqeDB6lDtXZBhkyHILKM9cbQmNYX75Eb9RKXRQAfMzFfg2UUtw; cf_clearance=ck0UImgR_4ZUWy2Is.4mSlOfaZMycvXnBqHngvK9R1I-1732395348-1.2.1.1-eNJgx5hhoCXqMAbzzZPGtXXLnPVLzNXJU0POeU7ZlFwdNFCQYpzc6R6ov91Y78tbGH5zfbcD0QTDcDjorm3Cr7i4hIFiQ6dnWBpU5OdQVK.tQ.p3n9URovf5v346uQCRztIVWv40IJLRIsT4eF7IL1gtqIG2XI42Ubv96Qev_l3K_InW0bmL0y2uhEn4453tgosr6uSwZrDFFHOCjs9LjJLLsAKyfl0Rgq5D3BqRDlS4ww1ubI2j.p_e3R6HGRI6uLHN9fU1om4q6UAjc96aBqKP7YKK3tGY.3zthOF2Wr3iImeKHDLpdtuglwiIyiq.UndhCr77NooIjjSwVwIiXREdqStV66Up.328UjZ0WuTiDk9NvQGWkeead_GNa9Q3; FindWorkHome:freelancerMenuSpacing=222px; umq=766; XSRF-TOKEN=4ce2dd2731b080d7ff8f6d0b5a2914c0; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Nov+23+2024+22%3A02%3A18+GMT%2B0100+(Central+European+Standard+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=93b7a6b5-269f-4e2a-a138-e567da63974c&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&AwaitingReconsent=false&geolocation=FR%3BIDF; asct_vt=oauth2v2_d9e586f597551198ecb604eba84a2592; forterToken=a21d7a42538942a0bd40278ea67681ed_1732395738384_621_UDF43-m4_23ck_uzVeTpQioCY%3D-4455-v2; forterToken=a21d7a42538942a0bd40278ea67681ed_1732395738384_621_UDF43-m4_23ck_uzVeTpQioCY%3D-4455-v2; _upw_id.5831=ecd04c2c-419b-4b62-88d9-59bbd7be7257.1730645905.8.1732395743.1732388258.288bf74c-a761-40ec-8c75-80e3f536dbce.43f9bd26-784c-4d5b-b696-a4b00d764516.297b9831-4834-439c-af2b-7235520c1d95.1732393321369.213; AWSALB=yRLTJLNH4is2pM0b6Ok9/NqC0iU74gbOdKAHiwCjC6NadvD7cy1B75L+fgGLphbOxMk97lDzbwAj7O/61Ck+qtjKBjlDBCA+wppoG2SdACn1hyI3TaJjlOf67yzq; AWSALBCORS=yRLTJLNH4is2pM0b6Ok9/NqC0iU74gbOdKAHiwCjC6NadvD7cy1B75L+fgGLphbOxMk97lDzbwAj7O/61Ck+qtjKBjlDBCA+wppoG2SdACn1hyI3TaJjlOf67yzq; enabled_ff=!RMTAir3Talent,i18nOn,!RMTAir3Offer,!MP16400Air3Migration,SSINavUserBpa,!CI10270Air2Dot5QTAllocations,!CI10857Air3Dot0,air2Dot76,!CI12577UniversalSearch,CI17409DarkModeUI,OTBnrOn,!i18nGA,JPAir3,TONB2256Air3Migration,!RMTAir3Home,CI11132Air2Dot75,!RMTAir3Hired,!air2Dot76Qt,!RMTAir3Offers,CI9570Air2Dot5,!SSINavUser",
    "origin": "https://www.upwork.com",
    "priority": "u=1, i",
    "referer": "https://www.upwork.com/ab/account-security/login",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-full-version-list": "\"Chromium\";v=\"130.0.6723.116\", \"Google Chrome\";v=\"130.0.6723.116\", \"Not?A_Brand\";v=\"99.0.0.0\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-ch-viewport-width": "766",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-odesk-csrf-token": csrf_token,
    "x-requested-with": "XMLHttpRequest"
}

# Define the payload for the login request
login_payload = {
    "username": LOGIN,
    "password": PASSWORD,
    "csrf_token": csrf_token
    
}

# Send the login request
login_response = session.post(login_url, headers=login_headers, data=login_payload)

# Check if login was successful
if login_response.status_code == 200:
    print("Login successful")

    # Define the headers for the scraping request
    scraping_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,fr;q=0.8",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    # Define the payload for the scraping request
    scraping_payload = {
        "query": """
        query($limit: Int, $toTime: String) {
            mostRecentJobsFeed(limit: $limit, toTime: $toTime) {
                results {
                    id,
                    uid:id
                    title,
                    ciphertext,
                    description,
                    type,
                    recno,
                    freelancersToHire,
                    duration,
                    engagement,
                    amount {
                        amount,
                    },
                    createdOn:createdDateTime,
                    publishedOn:publishedDateTime,
                    prefFreelancerLocationMandatory,
                    connectPrice,
                    client {
                        totalHires
                        totalSpent
                        paymentVerificationStatus,
                        location {
                            country,
                        },
                        totalReviews
                        totalFeedback,
                        hasFinancialPrivacy
                    },
                    tierText
                    tier
                    tierLabel
                    proposalsTier
                    enterpriseJob
                    premium,
                    jobTs:jobTime,
                    attrs:skills {
                        id,
                        uid:id,
                        prettyName:prefLabel
                        prefLabel
                    }
                    hourlyBudget {
                        type
                        min
                        max
                    }
                    isApplied
                },
                paging {
                    total,
                    count,
                    resultSetTs:minTime,
                    maxTime
                }
            }
        }
        """,
        "variables": {
            "limit": 10
        }
    }

    # Send the scraping request
    scraping_response = session.post(scraping_url, headers=scraping_headers, json=scraping_payload)

    # Check if scraping was successful
    if scraping_response.status_code == 200:
        data = scraping_response.json()
        print(data)
    else:
        print(f"Failed to fetch data: {scraping_response.status_code}")
else:
    print(f"Login failed: {login_response.status_code}")