def is_power(n):
    '''
    Returns true if n is a power of 2
    '''
    n = n/2
    if n == 2:
        return True
    elif n > 2:
        return is_power(n)
    else:
        return False
