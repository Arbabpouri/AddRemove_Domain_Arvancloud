from typing import Optional
import requests
import json


__BASE_API_URL__ = 'https://napi.arvancloud.ir/cdn/4.0'
__API_KEY__ = ""
__DEFAULT_HEADERS__ = {
    'Authorization': f'ApiKey {__API_KEY__}',
    'Content-Type': 'application/json'
}
__DOMAINS__ = [
    
]

# region records

def add_record(domain: str, record_type: Optional[str] = "aaaa", name: Optional[str] = "www") -> bool:

    api_url = f"{__BASE_API_URL__}/domains/{domain}/dns-records"
    data = {
        "value": [
            {
            "ip": "2a12:5940:dc12::2",
            "port": 1,
            "weight": 1000,
            "country": "US"
            }
        ],
        "type": str(record_type),
        "name": str(name),
        "ttl": 120,
        "cloud": False,
        "upstream_https": "auto",
        "ip_filter_mode": {
            "count": "single",
            "order": "none",
            "geo_filter": "none"
        }
    }

    response = requests.post(
        url=api_url,
        data=json.dumps(data),
        headers=__DEFAULT_HEADERS__,
        verify=False,
        allow_redirects=False
    )

    if response.status_code != 201: 
        return False
    
    if response.json().get('data', None):
        
        return True

    return False


# endregion

# region domains

def add_domain(domain: str, domain_type: Optional[str] = "full", plan_level: Optional[int] = 1) -> bool:
    
    api_url = f"{__BASE_API_URL__}/domains/dns-service"
    data = {
        "domain": str(domain),
        "domain_type": str(domain_type),
        "plan_level": int(plan_level)
    }

    response = requests.post(
        url=api_url,
        data=json.dumps(data),
        headers=__DEFAULT_HEADERS__,
        allow_redirects=False,
        verify=False
    )
    print(response.status_code)
    if response.status_code != 201: 
        return False
    
    if data := response.json().get('data', None):
        
        if data.get('id', None):

            if add_record(domain=domain):
                return True
            else:
                remove_domain(domain=domain)

    return False


def get_domain_id(domain: str) -> int | None:

    api_url = f"{__BASE_API_URL__}/domains/{domain}"

    response = requests.get(
        url=api_url,
        headers=__DEFAULT_HEADERS__,
        verify=False,
        allow_redirects=False
    )

    if response.status_code != 200: 
        return None
    
    if data := response.json().get('data', None):
        
        if domain_id := data.get('id', None):
            
            return domain_id

    return None


def remove_domain(domain: str) -> bool:

    domain_id = get_domain_id(domain=domain)
    
    if not domain_id:
        return False
    
    api_url = f"{__BASE_API_URL__}/domains/{domain}?id={domain_id}"

    response = requests.delete(
        url=api_url,
        headers=__DEFAULT_HEADERS__,
        verify=False,
        allow_redirects=False
    )

    if response.status_code == 200: 
        return True

    return False

# endregion


if __name__ == "__main__":
    for domain in __DOMAINS__:
        print("remove domain : ", remove_domain(domain=domain))
        print("add domain : ", add_domain(domain=domain))
