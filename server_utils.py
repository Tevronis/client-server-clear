

def merge_two_dicts(x, y):
    z = x.copy()   # start with x keys and values
    z.update(y)    # modifies z with y keys and values & returns None
    return z