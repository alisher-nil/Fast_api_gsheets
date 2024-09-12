from sqlalchemy import event

from app.models import CharityProject, Donation


def close_fund_if_goal_reached(target, value, oldvalue, initiator):
    if value == target.full_amount:
        target.close()


event.listen(Donation.invested_amount, "set", close_fund_if_goal_reached)
event.listen(CharityProject.invested_amount, "set", close_fund_if_goal_reached)
