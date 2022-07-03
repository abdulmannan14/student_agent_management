from .models import StudentModel
from Agent.models import AgentModel


def check_grater_or_lesser(fee_amount, previous_fee_amount):
    if fee_amount > previous_fee_amount:
        new_fee_amount_to_add = fee_amount - previous_fee_amount
    elif fee_amount < previous_fee_amount:
        new_fee_amount_to_add = fee_amount - previous_fee_amount
    else:
        new_fee_amount_to_add = 0

    return new_fee_amount_to_add


def calculate_gst_if_applicable(commission, student_obj):
    agent = student_obj.agent_name
    if agent.gst_status == AgentModel.EXCLUSIVE:
        gst_amount = (commission / 100) * agent.gst
    else:
        return 0
    return gst_amount


def calculate_commission_including_gst_and_commission(student_obj, fee_amount):
    commission = student_obj.agent_name.commission * (fee_amount / 100)
    gst = calculate_gst_if_applicable(commission, student_obj)
    new_commission = float(commission) + float(gst)
    return new_commission
