
CREATE TABLE "product" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255),
    "description" TEXT,
    "original_price" FLOAT,
    "liquidation_price" FLOAT,
    "front_view_path" VARCHAR(255),
    "back_view_path" VARCHAR(255),
    "register_date" TIMESTAMP,
    "state" VARCHAR(1),
    "category_fk" INTEGER REFERENCES "category"("id")
);
