def edit_phone(phone):
    phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')

    if len(phone) <= 10:
        phone = '+7' + phone
    elif phone.startswith('8'):
        phone = '+7' + phone[1:]
    elif phone.startswith('7'):
        phone = '+' + phone
    elif not phone.startswith('+7'):
        phone = '+7' + phone

    return phone
