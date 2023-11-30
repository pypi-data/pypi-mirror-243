import logging
import dotenv
import os


def load_envs(env_path:str, test: bool = True) -> tuple:
    """
    Load environment variables from a .env file.

    If the test parameter is True, it returns the test variables, otherwise it returns the production variables.

    Args:
        test (bool): A flag to determine if the function should return test or production variables. Defaults to True.

    Returns:
        tuple: A tuple containing the values of the environment variables.
    """
    dotenv.load_dotenv(env_path)
    if test:
        NOTION_KEY = os.getenv("TEST_NOTION_KEY")
        DAILY_DATA_ID = os.getenv("TEST_DAILY_DATA_ID")
        WEEKLY_DATA_ID = os.getenv("TEST_WEEKLY_DATA_ID")
        MONTHLY_DATA_ID = os.getenv("TEST_MONTHLY_DATA_ID")
        QUARTERLY_DATA_ID = os.getenv("TEST_QUARTERLY_DATA_ID")
        YEARLY_DATA_ID = os.getenv("TEST_YEARLY_DATA_ID")
        return (NOTION_KEY, DAILY_DATA_ID, WEEKLY_DATA_ID, MONTHLY_DATA_ID, QUARTERLY_DATA_ID, YEARLY_DATA_ID)
    else:
        NOTION_KEY = os.getenv("NOTION_KEY")
        DAILY_DATA_ID = os.getenv("DAILY_DATA_ID")
        WEEKLY_DATA_ID = os.getenv("WEEKLY_DATA_ID")
        MONTHLY_DATA_ID = os.getenv("MONTHLY_DATA_ID")
        QUARTERLY_DATA_ID = os.getenv("QUARTERLY_DATA_ID")
        YEARLY_DATA_ID = os.getenv("YEARLY_DATA_ID")
        return (NOTION_KEY, DAILY_DATA_ID, WEEKLY_DATA_ID, MONTHLY_DATA_ID, QUARTERLY_DATA_ID, YEARLY_DATA_ID)


def logging_setup() -> logging.Logger:
    """
    Set up a logger with a specific format and level.

    The logger logs messages to the console.

    Returns:
        logging.Logger: A logger instance.
    """
    logger = logging.getLogger('add_weeks')
    Fmt = logging.Formatter(fmt='%(asctime)s %(levelname)-8s (%(module)s:%(funcName)s:%(lineno)d): %(message)s', datefmt='%H:%M')  # lowercase var name, since it is an object

    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(Fmt)
    logger.addHandler(console)
    return logger

