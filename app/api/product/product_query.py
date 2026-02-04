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
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

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

    @strawberry.field
    async def get_one_product(self, slug: str) -> Optional[ProductType]:
        product = await product_collection.find_one({"slug": slug})

        if not product:
            raise Exception("No product found!")
        
        return ProductType(
            id=str(product["_id"]),
            title=product.get("title", "Unknown"),
            slug=product.get("slug"),
            desc=product.get("desc"),
            img=product.get("img"),
            category=product.get("category"),
            price=float(product.get("price", 0.0)),
            availableQty=int(product.get("availableQty", 0))
        )