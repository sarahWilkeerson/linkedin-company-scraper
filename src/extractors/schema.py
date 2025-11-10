from typing import TypedDict, Optional, List, Dict

class PostalAddress(TypedDict, total=False):
    type: str
    streetAddress: Optional[str]
    addressLocality: Optional[str]
    addressRegion: Optional[str]
    postalCode: Optional[str]
    addressCountry: Optional[str]

class StockInfo(TypedDict, total=False):
    symbol: Optional[str]
    price: Optional[str]
    change: Optional[str]

class AffiliatedPage(TypedDict, total=False):
    name: Optional[str]
    industry: Optional[str]
    address: Optional[str]
    linkedinUrl: Optional[str]

class CompanyRecord(TypedDict, total=False):
    name: Optional[str]
    url: Optional[str]
    mainAddress: PostalAddress
    description: Optional[str]
    numberOfEmployees: Optional[int]
    logo: Optional[str]
    website: Optional[str]
    industry: Optional[str]
    companySize: Optional[str]
    headquarters: Optional[str]
    type: Optional[str]
    founded: Optional[int]
    specialties: Optional[str]
    followersCount: Optional[int]
    stock: StockInfo
    addresses: List[str]
    affiliatedPages: List[AffiliatedPage]
    similarPages: List[AffiliatedPage]
    rawHtml: Optional[str]
    scrapedAt: Optional[str]