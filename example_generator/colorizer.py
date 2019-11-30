def colorizer():
    """

    colorizer creates colors to be used in full_imager. It is here to avoid making full_imager even more confusing.

    :return: A list of colors represented by 6 character strings of hexadecimal digits (rrggbb).
    """

    colors = []
    for r in ["00", "10", "20", "30", "40", "50", "60", "70", "80", "90", "A0", "B0", "C0", "D0", "E0", "F0", "FF"]:
        for g in ["00", "10", "20", "30", "40", "50", "60", "70", "80", "90", "A0", "B0", "C0", "D0", "E0", "F0", "FF"]:
            for b in ["00", "10", "20", "30", "40", "50", "60", "70", "80", "90", "A0", "B0", "C0", "D0", "E0", "F0",
                      "FF"]:
                colors.append(r+g+b)
    return colors
