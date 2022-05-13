



def check_grater_or_lesser(fee_amount, previous_fee_amount):
    if fee_amount > previous_fee_amount:
        new_fee_amount_to_add = fee_amount - previous_fee_amount
    elif fee_amount < previous_fee_amount:
        new_fee_amount_to_add = fee_amount - previous_fee_amount
    else:
        new_fee_amount_to_add = 0

    return new_fee_amount_to_add