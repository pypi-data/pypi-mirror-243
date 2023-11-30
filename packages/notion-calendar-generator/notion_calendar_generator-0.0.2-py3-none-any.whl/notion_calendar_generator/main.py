import click
import importlib.metadata
import logging

from notion_calendar_generator.notion import API
from notion_calendar_generator.calendar_generator import Calendar
from notion_calendar_generator.utils import logging_setup, load_envs

logger = logging_setup()
package_name = "notion-calendar-generator"

try:
    version = importlib.metadata.version(package_name)
except importlib.metadata.PackageNotFoundError:
    version = 'unknown'


def generate_calendar(notion: API, calendar: Calendar, logger_instance: logging.Logger = logger) -> None:
    """
    Generate a calendar.

    Args:
        notion (API): An instance of the API class.
        calendar (Calendar): An instance of the Calendar class.
        logger_instance (logging.Logger): A logger instance. Defaults to the logger set up at the start of this file.
    """
    logger_instance.info('create year')
    year_page_id = notion.post_page(notion.year_id, calendar.year)

    logger_instance.info('create quarters')
    calendar.update_quarters(year_page_id)
    quarter_page_ids = notion.post_page(notion.quarter_id, calendar.quarters)

    logger_instance.info('create months')
    calendar.update_months(year_page_id, quarter_page_ids)
    month_page_ids = notion.post_page(notion.month_id, calendar.months)

    logger_instance.info('create weeks')
    calendar.update_weeks(month_page_ids)
    week_page_ids = notion.post_page(notion.week_id, calendar.weeks)

    logger_instance.info('create days')
    calendar.update_days(week_page_ids)
    notion.post_page(notion.day_id, calendar.days)


@click.command()
@click.version_option(version, prog_name="notion-page-generator")
@click.argument("year", type=int)
@click.option("--env-path", default=".env", help="Path to the .env file. Defaults to .env.")
@click.option('--test', default=False, is_flag=True, help='Run in test mode against a different set of databases.')
def main(year: int, env_path: str = ".env", test: bool = True, logger_instance: logging.Logger = logger) -> None:
    """
    The main function.

    Args:
        env_path (str): Path to the .env file. Defaults to ".env".
        year (int): The year for which to generate the calendar.
        test (bool): A flag to determine if the function should run in test mode. Defaults to True.
        logger_instance (logging.Logger): A logger instance. Defaults to the logger set up at the start of this file.
    """
    logger_instance.info("loading API KEYS")
    (NOTION_KEY, DAILY_DATA_ID, WEEKLY_DATA_ID, MONTHLY_DATA_ID, QUARTERLY_DATA_ID, YEARLY_DATA_ID) = load_envs(
        env_path,
        test=test)

    url = "https://api.notion.com/v1/pages"
    headers = {
        'Authorization': f"Bearer {NOTION_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16',
    }
    logger_instance.info('loaded url and header')
    notion = API(url, headers, logger_instance)
    notion.add_connection_strs(DAILY_DATA_ID, WEEKLY_DATA_ID, MONTHLY_DATA_ID, QUARTERLY_DATA_ID, YEARLY_DATA_ID)
    calendar = Calendar(year)
    generate_calendar(notion, calendar)


if __name__ == "__main__":
    main()
