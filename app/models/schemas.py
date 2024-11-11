from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class SalesMetrics(BaseModel):
    total_sales: float
    average_ticket: float
    total_customers: int
    total_transactions: int
    period_start: datetime
    period_end: datetime

class ProductAnalytics(BaseModel):
    product_code: str
    description: str
    total_quantity: int
    total_revenue: float
    category: str
    price_category: str

class CountryMetric(BaseModel):
    country: str
    customer_count: int
    average_spend: float

class CustomerSegment(BaseModel):
    segment_name: str
    customer_count: int
    average_value: float

class CustomerMetrics(BaseModel):
    total_unique_customers: int
    average_customer_value: float
    top_countries: List[CountryMetric]
    customer_segments: Dict[str, CustomerSegment]

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    database_connected: bool
    version: str