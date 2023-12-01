import json
import tomllib
import tomli_w
from contextlib import asynccontextmanager

from tortoise import Tortoise

from .models import TestRecord
from .entry import Entry


class ResultStore:
    async def add_result(self, test_name: str, application_name: str, data: dict):
        """Adds a result to the database. The pairs (test_name, application_name)
        are assumed to be unique"""
        await TestRecord.update_or_create(
            test_name=test_name,
            application_name=application_name,
            defaults={"data": data},
        )

    async def delete_record(self, test_name: str, application_name: str):
        """Deletes database record if exists"""
        record = await TestRecord.get_or_none(
            test_name=test_name,
            application_name=application_name,
        )
        if record:
            await record.delete()

    async def results_for_test(self, test_name: str) -> list:
        """Retrieves the results for a given test_name"""
        result = await TestRecord.filter(test_name=test_name).all()

        return [{"application_name": x.application_name, **x.data} for x in result]

    async def entry_for_test(self, test_name: str) -> Entry:
        result = await TestRecord.filter(test_name=test_name).all()

        return Entry({x.application_name: x.data for x in result})

    async def as_list(self) -> list:
        records = await TestRecord.filter().order_by("test_name", "application_name")

        return [
            {
                "test_name": record.test_name,
                "application_name": record.application_name,
                "data": json.dumps(record.data, indent=2),
            }
            for record in records
        ]

    async def load(self, filename: str = "test_results.toml"):
        """Deletes the current content from the database, then loads
        the content from filename to it."""

        await TestRecord.filter().delete()

        with open(filename, "rb") as fp:
            data = tomllib.load(fp)

        for x in data["entries"]:
            await self.add_result(
                test_name=x["test_name"],
                application_name=x["application_name"],
                data=json.loads(x["data"]),
            )

    async def save(self, filename: str = "test_results.toml"):
        """Saves the content of the database to the file given by filename"""

        with open(filename, "wb") as fp:
            tomli_w.dump({"entries": await self.as_list()}, fp, multiline_strings=True)


@asynccontextmanager
async def with_store(db_url="sqlite://test_results.sqlite") -> ResultStore:
    """Initializes the database and returns a ResultStore. Usage:

    ```python
    async with with_store() as store:
        await store.add_result(...)
        ...
        await store.results_for_test(...)
    ```
    """
    await Tortoise.init(
        config={
            "connections": {"default": db_url},
            "apps": {
                "models": {
                    "models": [
                        "fediverse_pasture.runner.models",
                    ],
                    "default_connection": "default",
                },
            },
        },
    )
    await Tortoise.generate_schemas()

    yield ResultStore()

    await Tortoise.close_connections()
