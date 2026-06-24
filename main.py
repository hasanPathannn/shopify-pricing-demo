from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Shopify Pricing Rules API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pricing-demo-bhkp2bt9.myshopify.com", 
        "*" 
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected request payload
class PricingRequest(BaseModel):
    zip_code: str
    product_id: str

# Hardcoded rules engine as requested
PRICING_RULES = {
    "75028": 1499.00,
    "10001": 1699.00,
    "90210": 1799.00
}

# Default fallback price
DEFAULT_PRICE = 1299.00 

@app.post("/api/get-price")
def get_price(request: PricingRequest):
    # Clean the input
    zip_code = request.zip_code.strip()
    
    # Check if the ZIP exists in our rules engine
    if zip_code in PRICING_RULES:
        return {
            "status": "success", 
            "zip_code": zip_code, 
            "price": PRICING_RULES[zip_code],
            "message": "Custom regional pricing applied."
        }
    else:
        # Graceful fallback for unknown ZIP codes
        return {
            "status": "success", 
            "zip_code": zip_code, 
            "price": DEFAULT_PRICE, 
            "message": "Standard pricing applied."
        }