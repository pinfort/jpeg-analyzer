def colors(nf):
    if nf == 1:
        return ["Y"]
    elif nf == 2:
        return ["Y", "A"]
    elif nf == 3:
        return ["Y", "Cb", "Cr"]
    elif nf == 4:
        return ["Y", "Cb", "Cr", "A"]
    else:
        raise ValueError("invalid value")
