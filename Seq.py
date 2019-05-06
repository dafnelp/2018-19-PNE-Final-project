# Creating a class
class Seq:
    def __init__(self, strbases):
        # initialize the sequence with the value passed as argument when creating the object
        self.strbases = strbases

    def len(self):
        """ Function for calculating the length"""
        return len(self.strbases)

    def perc(self, base):
        """ Function for calculating the percentage of the bases"""
        # Percentage of A
        if base == "A":
            perc_a = "{} %".format(round(100.0 * self.strbases.count('A') / len(self.strbases), 1))
            return perc_a

        # Percentage of C
        elif base == "C":
            perc_c = "{} %".format(round(100.0 * self.strbases.count('C') / len(self.strbases), 1))
            return perc_c

        # Percentage of T
        elif base == "T":
            perc_t = "{} %".format(round(100.0 * self.strbases.count('T') / len(self.strbases), 1))
            return perc_t

        # Percentage of G
        elif base == "G":
            perc_g = "{} %".format(round(100.0 * self.strbases.count('G') / len(self.strbases), 1))
            return perc_g
