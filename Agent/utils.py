



def check_grater_or_lesser(current_commission_amount, previous_commission_amount):
    if current_commission_amount > previous_commission_amount:
        new_commission_amount_to_add = current_commission_amount - previous_commission_amount
    elif previous_commission_amount < previous_commission_amount:
        new_commission_amount_to_add = current_commission_amount - previous_commission_amount
    else:
        new_commission_amount_to_add = 0

    return new_commission_amount_to_add