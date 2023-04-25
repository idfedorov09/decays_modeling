import json
import random
from sympy import preview
from tqdm import tqdm


class MyParticle:

    def __init__(self, particle):
        with open("data.json", "r") as file:
            json_contain = file.read()
            particle_info = json.loads(json_contain)
        if particle not in particle_info:
            raise Exception("I can't find a {} particle in my database :\\".format(particle))
        self.decays = particle_info[particle]
        self.particle = particle

    def gen_probability_by_num(self, num):
        p = self.decays[num]["probability_wm"] * 10 ** (self.decays[num]["log_mantiss"]) * 10 ** (-2)
        dp = self.decays[num]["delta_wm"] * 10 ** (self.decays[num]["log_mantiss"]) * 10 ** (-2)
        return random.gauss(p, dp)

    def gen_distribution(self):
        probabilities = {decay_res["latex"]: 0 for decay_res in self.decays}

        last = 0
        for i in range(len(self.decays)):
            prob = self.gen_probability_by_num(i) + last
            last = prob
            probabilities[self.decays[i]["latex"]] = prob

        return probabilities

    def gen(self, count_of_particles, with_open=True, progress_bar=True, dpi=1200):
        res = {decay_res["latex"]: 0 for decay_res in self.decays}
        res["$mbox{Other decays}"] = 0

        to_iter = range(count_of_particles)
        if progress_bar:
            to_iter = tqdm(to_iter, colour="#00d746")

        for _ in to_iter:
            fake_distribution = self.gen_distribution()

            max_p = 1
            for i in fake_distribution:
                max_p = max(max_p, fake_distribution[i])

            fake_distribution = {i: fake_distribution[i] / max_p for i in fake_distribution}

            rand_value = random.random()

            ok = False
            for i in fake_distribution:
                if rand_value <= fake_distribution[i]:
                    res[i] += 1
                    ok = True
                    break

            if not ok:
                res["$mbox{Other decays}"] += 1

        res["$mbox{Total}"] = count_of_particles
        if with_open:
            self.gen_image(self.res_to_tex(res, count_of_particles), dpi)

        return res

    def res_to_tex(self, ans_list, total):
        text = '''
                \\documentclass[preview, border = 5pt]{{standalone}}\n\\begin{{document}}\n\
                \\begin{{center}}The result of modeling the decays of {particle} particles:\\end{{center}}
                '''.format(particle=self.particle)

        for i in ans_list:
            cur = i.replace("$", "\\")
            text += "$$"
            text += cur + ": \\quad " + str(ans_list[i])
            if "Total" not in cur:
                text += ",\\quad " + self.format_number(ans_list[i] / total)
            text += "\\\\"
            text += "$$"

        return text

    @staticmethod
    def format_number(x):
        a, b = '{:.3e}'.format(x).split('e')
        b = str(int(b) + 2)
        if a == '0.000':
            return "0 \%"
        if int(b) == 0:
            return f'{float(a):.3f}\\%'
        if int(b) == 1:
            return '{:.3f} \%'.format(x * 100)
        return f'{float(a):.3f}\\cdot 10^{{{int(b)}}}\\%'

    @staticmethod
    def gen_image(latex_string, dpi):
        preview('', output='png', preamble=latex_string, dvioptions=['-D', str(dpi)])
