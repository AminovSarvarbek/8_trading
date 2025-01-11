from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_premium" INT   DEFAULT 0;
        CREATE TABLE IF NOT EXISTS "channel" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" BIGINT NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_premium";
        DROP TABLE IF EXISTS "channel";"""
