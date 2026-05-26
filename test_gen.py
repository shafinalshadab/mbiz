"""Test the generation pipeline with language parameter."""
import asyncio
import json
from ai_engine import generate_facebook_content

async def test():
    result = await generate_facebook_content(
        product_name="LuxeFit Slim Blazer",
        product_category="Men's Fashion",
        core_usp="Stretch fabric, wrinkle-free, tailored fit for Bangladeshi men",
        target_location="Dhaka, Bangladesh",
        target_audience="Professional men aged 25-45",
        additional_context="Office wear. Price: ৳3,500",
        language_code="banglish",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))

asyncio.run(test())
