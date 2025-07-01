# dnb_app/utils.py

def get_category_desc(catg_num):
    """
    Map category numbers to category descriptions.
    DNB: 0-6
    CONTRACTUAL: 7-9, 13-14
    CSR: 10-12
    """
    if 0 <= catg_num <= 6:
        return 'DNB'
    elif catg_num in [7, 8, 9, 13, 14]:
        return 'CONTRACTUAL'
    elif 10 <= catg_num <= 12:
        return 'CSR'
    return ''

def get_valid_category_numbers():
    """Return list of all valid category numbers for DNB, CONTRACTUAL, CSR."""
    return list(range(0, 7)) + [7, 8, 9, 13, 14] + list(range(10, 13))

def is_valid_category(catg_num):
    """Check if category number is valid for DNB, CONTRACTUAL, or CSR."""
    return catg_num in get_valid_category_numbers()
