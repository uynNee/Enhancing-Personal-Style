# Personal Color Type Classification (Modified File)
# Initial Creation Date: 20/04/23
# Author: Yesul Cho
#
# Description:
#
#         After readjusting the criteria for personal color types

# Function
# Classify according to the criteria

# Class
# Classify according to the criteria

class Color:
    person_HSV = []

    def color_classifier(self, person_HSV):
        self.H = float(person_HSV[0])
        self.S = float(person_HSV[1])
        self.V = float(person_HSV[2])
        diff = round(self.V - self.S, 2)

        color_type = ["WSB", "WSL", "WAD", "WAM", "CSL", "CSM", "CWB", "CWD"]

        if 23 <= self.H <= 203:
            if diff >= 46.25:
                if self.S >= 31.00:
                    self.ans = 0
                    # Warm Spring Bright
                else:
                    self.ans = 1
                    # Warm Spring Light

            elif diff < 46.25:
                if self.S >= 46.22:
                    self.ans = 2
                    # Warm Autumn Deep
                else:
                    self.ans = 3
                    # Warm Autumn Mute

        elif (0 <= self.H < 23) or (203 < self.H <= 360):
            if diff >= 48.75:
                if diff >= 28.47:
                    self.ans = 4
                    # Cool Summer Light
                else:
                    self.ans = 5
                    # Cool Summer Mute

            elif diff < 48.75:
                if diff >= 31.26:
                    self.ans = 6
                    # Cool Winter Bright
                else:
                    self.ans = 7
                    # Cool Winter Deep

        else:
            self.ans = -1
            # Error

        return self.ans
