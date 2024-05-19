# Personal Color Type Classification (Original File)
# Initial creation date: 20/02/11
# Author: Yesul Cho
#
# Description: Classify personal color types based on HSV
#
# Modification History:
#     20/02/19
#         - Changed classification criteria from Munsell to HSV
#
#     20/02/20
#         - Assigned numerical values to personal color type results, rearranged return statements, adjusted type criteria (Detail of Cool)
#
#     20/02/24
#         - Added class format
#
#     20/02/25
#         - Added class format return, removed unnecessary functions
#
#     20/03/04
#         - Written as a PyCharm file
#
#     20/03/05
#         - Corrected mathematical errors
#
#     20/03/08
#         - Adjusted H range


# Functions
# Classify based on criteria

# Class
# Classify based on criteria

class Color:
    person_HSV = []
        
    def color_classifier(self, person_HSV):
        self.H = float(person_HSV[0])
        self.S = float(person_HSV[1])
        self.V = float(person_HSV[2])
        diff = round(self.V - self.S, 2)
    
        color_type = ["WSB", "WSL", "WAD", "WAM", "CSL", "CSM", "CWB", "CWD"]

        if 23 <= self.H <= 203:
            if diff >= 43.15:
                if self.S >= 32.47:
                    self.ans = 0
                    # Warm Spring Bright                            
                else:
                    self.ans = 1
                    # Warm Spring Light

            elif diff < 43.15:
                if self.S >= 32.47:
                    self.ans = 2
                    # Warm Autumn Deep                
                else:
                    self.ans = 3
                    # Warm Autumn Mute

        elif (0 <= self.H < 23) or (203 < self.H <= 360):
            if diff >= 47.15:
                if diff >= 60.80:
                    self.ans = 4
                    # Cool Summer Light                
                else:
                    self.ans = 5
                    # Cool Summer Mute

            elif diff < 47.15:
                if diff >= 23.58:
                    self.ans = 6
                    # Cool Winter Bright                
                else:
                    self.ans = 7
                    # Cool Winter Deep

        else:
            self.ans = -1
            # Error
            
        return self.ans
