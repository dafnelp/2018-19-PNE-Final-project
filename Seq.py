class Seq:
    def __init__(self, strbases):

        self.strbases = strbases

    def len(self):

        return len(self.strbases)

    def perc(self, base):
        if base == "A":
            perc_a = "{} %".format(round(100.0 * self.strbases.count('A') / len(self.strbases), 1))
            return perc_a

        elif base == "C":
            perc_c = "{} %".format(round(100.0 * self.strbases.count('C') / len(self.strbases), 1))
            return perc_c

        elif base == "T":
            perc_t = "{} %".format(round(100.0 * self.strbases.count('T') / len(self.strbases), 1))
            return perc_t

        elif base == "G":
            perc_g = "{} %".format(round(100.0 * self.strbases.count('G') / len(self.strbases), 1))
            return perc_g
