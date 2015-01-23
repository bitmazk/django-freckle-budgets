"""Test-fixtures for the freckle_budgets app."""
from mixer.backend.django import mixer


def create_month(cls):
    """Creates one ``Month`` object."""
    cls.year = mixer.blend(
        'freckle_budgets.Year', year=2015, sick_leave_days=12,
        vacation_days=12, rate=100)
    cls.month = mixer.blend(
        'freckle_budgets.Month', month=1, year=cls.year, public_holidays=1,
        employees=2)


def create_project_months(cls):
    """Creates two ``ProjectMonth`` objects."""
    create_month(cls)
    cls.month2 = mixer.blend(
        'freckle_budgets.Month', month=2, year=cls.year, public_holidays=1,
        employees=2)
    cls.proj1 = mixer.blend(
        'freckle_budgets.Project', is_investment=False, freckle_project_id='1')
    cls.proj2 = mixer.blend(
        'freckle_budgets.Project', is_investment=True, freckle_project_id='2')

    cls.project_month1_1 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj1,
        month=cls.month, budget=1000, rate=100, )
    cls.project_month2_1 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj1,
        month=cls.month2, budget=2000, rate=100, )

    cls.project_month1_2 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj2,
        month=cls.month, budget=4000, rate=200, )


def get_api_response(cls):
    """
    Returns a typical freckle API response and creates necessary objects.

    """
    cls.year = mixer.blend('freckle_budgets.Year', year=2015)
    cls.month1 = mixer.blend('freckle_budgets.Month', month=1, year=cls.year)
    cls.month2 = mixer.blend('freckle_budgets.Month', month=2, year=cls.year)
    cls.proj1 = mixer.blend(
        'freckle_budgets.Project', freckle_project_id='111')
    cls.proj2 = mixer.blend(
        'freckle_budgets.Project', freckle_project_id='222')
    cls.proj3 = mixer.blend(
        'freckle_budgets.Project', freckle_project_id='333',
        is_investment=True)

    cls.proj1_month1 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj1, month=cls.month1,
        budget=1000, rate=100)
    cls.proj1_month2 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj1, month=cls.month2,
        budget=1000, rate=100)
    cls.proj2_month1 = mixer.blend(
        'freckle_budgets.projectmonth', project=cls.proj2, month=cls.month1,
        budget=2000, rate=200)
    cls.proj2_month2 = mixer.blend(
        'freckle_budgets.projectmonth', project=cls.proj2, month=cls.month2,
        budget=2000, rate=200)
    cls.proj3_month1 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj3, month=cls.month1,
        budget=4000, rate=400)
    cls.proj3_month2 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj3, month=cls.month2,
        budget=4000, rate=400)

    entries = [
        {
            # First project, first month, billable hours
            'entry': {
                'date': '2015-01-01',
                'project_id': 111,
                'billable': True,
                'minutes': 1,
            }
        },
        {
            # Unbillable hours should not be added up
            'entry': {
                'date': '2015-01-01',
                'project_id': 111,
                'billable': False,
                'minutes': 2,
            }
        },
        {
            # Billable hours should be added up
            'entry': {
                'date': '2015-01-01',
                'project_id': 111,
                'billable': True,
                'minutes': 4,
            }
        },
        {
            # Another project in the same month
            'entry': {
                'date': '2015-01-01',
                'project_id': 222,
                'billable': True,
                'minutes': 8,
            }
        },
        {
            # Another month
            'entry': {
                'date': '2015-02-01',
                'project_id': 222,
                'billable': True,
                'minutes': 16,
            }
        },
        {
            # Unbillable hours for investment projects should be added up
            'entry': {
                'date': '2015-02-01',
                'project_id': 333,
                'billable': False,
                'minutes': 32,
            }
        },
    ]
    return entries
