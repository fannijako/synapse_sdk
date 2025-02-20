import random


def create_test_delta(notebook):
    data = []
    names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    departments = ["HR", "IT", "Finance", "Marketing", "Sales"]

    for _ in range(1000):
        name = random.choice(names)
        age = random.randint(22, 65)
        salary = random.randint(30000, 150000)
        department = random.choice(departments)
        data.append((name, age, salary, department))

    path = f'{notebook.curated_path}/generic_utils/integration_test'
    test_curated_location = f'{path}/test_delta_listing_curated.delta'
    test_trusted_location = f'{notebook.trusted_path}/test_delta_listing_trusted.delta'

    (spark.createDataFrame(data, ["name", "age", "salary", "department"]) # type: ignore # pylint: disable=undefined-variable
          .write.format("delta")
          .mode("overwrite")
          .save(test_curated_location))
    (spark.createDataFrame(data, ["name", "age", "salary", "department"]) # type: ignore # pylint: disable=undefined-variable
          .write
          .format("delta")
          .mode("overwrite").save(test_trusted_location))

    return test_curated_location, test_trusted_location
