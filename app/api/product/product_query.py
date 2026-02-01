import strawberry
from typing import List, Optional
from app.database import db

product_collection = db.get_collection("products")

@strawberry.type
class ProductType:
    id: str
    title: str
    slug: str
    desc: Optional[str] = None
    img: Optional[str] = None
    category: str
    price: float
    availableQty: int
    createdAt: str
    updatedAt: str

@strawberry.type
class ProductQuery:
    @strawberry.field
    async def get_products(self, category: Optional[str] = None) -> List[ProductType]:
        query_filter = {}
        if category:
            query_filter["category"] = category

        products_cursor = product_collection.find(query_filter)

        products_list = []
        async for p in products_cursor:
            products_list.append(
                ProductType(
                    id=str(p["_id"]),
                    title=p.get("title", "Unknown"),
                    slug=p.get("slug"),
                    desc=p.get("desc", "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Eum molestiae quod totam cum facilis minima voluptatibus repellendus! Quasi minima commodi nobis ex, natus numquam dolorum repellat nam impedit repellendus et."),
                    img=p.get("img"),
                    category=p.get("category"),
                    price=float(p.get("price", 0.0)),
                    availableQty=int(p.get("availableQty", 0)),
                    createdAt=p.get("createdAt").isoformat() if p.get("createdAt") else "",
                    updatedAt=p.get("updatedAt").isoformat() if p.get("updatedAt") else ""
                )
            )

        return products_list
