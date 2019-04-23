class Seq:
    def __init__(self, strbases):

        self.strbases = strbases

    def len(self):

        return len(self.strbases)

    def count_bases(self, base):
        if base == "A":
            a_base = self.strbases.count("A")
            count_a = "A: {}".format(a_base)
            return count_a
        elif base == "C":
            c_base = self.strbases.count("C")
            count_c = "C: {}".format(c_base)
            return count_c
        elif base == "T":
            t_base = self.strbases.count("T")
            count_t = "T: {}".format(t_base)
            return count_t
        elif base == "G":
            g_base = self.strbases.count("G")
            count_g = "G: {}".format(g_base)
            return count_g

    def complement(self):

        base_complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
        c_seq = []

        for character in self.strbases:
            c_seq.append(base_complement[character])

        return ''.join(c_seq)

    def reverse(self):
        r_seq = []
        len_seq = len(self.strbases)

        for i in self.strbases:
            len_seq = len_seq - 1
            r_seq.append(self.strbases[len_seq])

        return ''. join(r_seq)

    def perc(self, base ):
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
