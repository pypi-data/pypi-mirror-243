import os
from xml2db import DataModel
from sqlalchemy import inspect

from tests.sample_models.models import models


def setup():
    model_config = models[2]

    model = DataModel(
        os.path.join("../", model_config["xsd_path"]),
        short_name="junit",
        model_config=model_config["versions"][0]["config"],
    )

    return model


def main():
    from sqlalchemy import create_engine

    connection_string = "mssql+pyodbc://DATACRE\DEV_BASECRE/BaseCRE?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

    engine = create_engine(
        "postgresql+psycopg2://testuser:testuser@localhost:5432/testdb"
    )

    inspector = inspect(engine)
    print("ok")


if __name__ == "__main__":
    main()
