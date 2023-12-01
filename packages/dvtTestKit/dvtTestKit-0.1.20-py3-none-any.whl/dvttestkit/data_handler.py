import sqlite3
from typing import List, Optional, Tuple


def create_test_results_table(conn: sqlite3.Connection) -> None:
    """
    Creates a test_results table in the specified SQLite database if it does not already exist.

    Args:
        conn: A SQLite database connection.

    Returns:
        None.
    """
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_version TEXT NOT NULL,
            device_model TEXT NOT NULL,
            test_id TEXT NOT NULL,
            test_name TEXT NOT NULL,
            test_runtime TEXT NOT NULL,
            test_last_result TEXT NOT NULL,
            number_of_fails INTEGER NOT NULL,
            number_of_passes INTEGER NOT NULL
        )
    """)
    conn.commit()


def test_create_test_results_table(database: str = "test_results.db") -> None:
    """
        Tests the create_test_results_table function by creating a test_results table in a SQLite database.

        test_name: A string representing the name of the Database.
        Returns:
            None.
        """
    conn = sqlite3.connect(database)
    create_test_results_table(conn)
    conn.close()


def insert_test_result(conn: sqlite3.Connection,
                       app_version: str,
                       device_model: str,
                       mac_address: Optional[str] = "None",
                       test_id: Optional[str] = "None",
                       test_name: Optional[str] = "None",
                       test_runtime: Optional[str] = "None",
                       test_last_result: Optional[str] = "None",
                       number_of_fails: Optional[int] = "0",
                       number_of_passes: Optional[int] = "0", ) -> None:
    """
    Inserts a new row into the test_results table with the specified values.

    Args:
        conn: A SQLite database connection.
        app_version: A string representing the version of the software being tested.
        device_model: A string representing the model of the DUT.
        mac_address: A strng representing the mac address of the DUT
        test_id: A string representing the Test identifier.
        test_name: A string representing the name of the test.
        test_runtime: A string representing the amount of time the test took to run.
        test_last_result: A string representing the result of the most recent test run.
        number_of_fails: An integer representing the number of times the test has failed.
        number_of_passes: An integer representing the number of times the test has passed.

    Returns:
        None.
    """
    c = conn.cursor()
    c.execute("""
        INSERT INTO test_results (app_version, device_model, mac_address, test_id, test_name, test_runtime, test_last_result, number_of_fails, number_of_passes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (app_version, device_model, mac_address, test_id, test_name, test_runtime,
          test_last_result, number_of_fails,
          number_of_passes))
    conn.commit()


def test_insert_test_result() -> None:
    """
    Tests the insert_test_result function by inserting a test result
    into a temporary SQLite database.

    Returns:
        None.
    """
    conn = sqlite3.connect(":memory:")  # Creates an in-memory SQLite database.
    create_test_results_table(
        conn)  # Creates the test_results table if it doesn't exist.
    insert_test_result(conn, "1.0", "Google Pixel 4", test_id="11",
                       test_name="Login Test",
                       test_runtime="2023-02-10 10:00:00",
                       test_last_result="PASS", number_of_fails=0,
                       number_of_passes=1)
    conn.close()


def retrieve_test_results(conn: sqlite3.Connection,
                          test_name: Optional[str] = None,
                          test_last_result: Optional[str] = None,
                          limit: Optional[int] = None) -> List[Tuple]:
    """
    Retrieves test results from the test_results table that match the given criteria.

    Args:
        conn: A connection to the SQLite database.
        test_name: The name of the test to retrieve results for.
        test_last_result: The last result of the test to retrieve results for.
        limit: The maximum number of results to retrieve.

    Returns:
        A list of tuples, where each tuple represents a row in the test_results table.
    """
    c = conn.cursor()
    query = "SELECT * FROM test_results"
    params: List = []
    if test_name is not None:
        query += " WHERE test_name=?"
        params.append(test_name)
    if test_last_result is not None:
        if len(params) == 0:
            query += " WHERE test_last_result=?"
        else:
            query += " AND test_last_result=?"
        params.append(test_last_result)
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)
    c.execute(query, params)
    return c.fetchall()


def test_retrieve_test_results() -> list[tuple]:
    """
    Tests the retrieve_test_results function by retrieving the first 5 test results with a last result of "PASS" and
    printing them to the console. Uses an in-memory database for testing.
    """
    conn = sqlite3.connect(":memory:")
    create_test_results_table(conn)
    insert_test_result(conn, "1.0", "Google Pixel 4", test_id="11",
                       test_name="Login Test",
                       test_runtime="2023-02-10 10:00:00",
                       test_last_result="PASS", number_of_fails=0,
                       number_of_passes=1)
    results = retrieve_test_results(conn, test_last_result="PASS", limit=5)
    for result in results:
        print(result)
    conn.close()
    return results


def check_for_missing_data(test_results: List[Tuple]) -> List[
    Tuple[int, Tuple]]:
    """
    Checks the given list of test results for any missing data (i.e. Default value of "None" ) and returns a list of tuples
    indicating the index of the missing data and the test result that contains it.

    :param test_results: A list of test results to check for missing data.
    :return: A list of tuples indicating the index of the missing data and the test result that contains it.
    """
    missing_data = []
    for test_result in test_results:
        for i, value in enumerate(test_result):
            if value == "None":
                missing_data.append((i, test_result))
                break
    return missing_data


def test_check_for_missing_data(database: str = ":memory:") -> List[Tuple[int, Tuple]]:
    """
    Tests the check_for_missing_data function by retrieving all test results from the in-memory database and calling the
    function to check for missing data. Returns the list of missing data tuples.
    """
    conn = sqlite3.connect(database)
    create_test_results_table(conn)
    insert_test_result(conn, "1.0", "Google Pixel 4", test_id="11",
                       test_name="Login Test",
                       test_runtime="2023-02-10 10:00:00",
                       test_last_result="PASS", number_of_fails=0,
                       number_of_passes=1)
    insert_test_result(conn, "1.0", "Google Pixel 5", test_id="12",
                       test_name="Login Test",
                       test_runtime="2023-02-11 12:00:00",
                       test_last_result="PASS", number_of_fails=0,
                       number_of_passes=1)
    insert_test_result(conn, "1.1", "Samsung Galaxy S10", test_id="10",
                       test_name="Signup Test",
                       test_runtime="2023-02-12 14:00:00",
                       test_last_result="None", number_of_fails=1,
                       number_of_passes=0)
    test_results = retrieve_test_results(conn)
    missing_data = check_for_missing_data(test_results)
    conn.close()
    return missing_data


if __name__ == '__main__':
    test_check_for_missing_data()
