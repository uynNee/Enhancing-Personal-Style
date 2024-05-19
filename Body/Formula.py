import math

# Conversion factors
INCH_TO_CM_FACTOR = 2.54

def convert_to_cm(inches):
    return inches * INCH_TO_CM_FACTOR

def classify_body_shape(gender, bust, waist, high_hip, hips):
    bust = convert_to_cm(bust)
    waist = convert_to_cm(waist)
    high_hip = convert_to_cm(high_hip)
    hips = convert_to_cm(hips)

    if gender.lower() == 'men':
        if (bust - hips) > 2.54 and (bust - hips) < 25.4 and (bust - high_hip) >= 22.86:
            return "Top Hourglass"
        elif (bust - hips) <= 2.54 and (hips - bust) <= 2.54 and (bust - waist) >= 12.7 and (hips - waist) >= 12.7:
            return "Bottom Hourglass"
        elif (hips - bust) >= 5.08 and (waist - bust) < 17.78:
            return "Triangle or Pear"
        elif (bust - hips) < 2.54 and (hips - bust) < 2.54 and (bust - waist) < 17.78 and (hips - waist) < 12.7:
            return "Rectangle or Banana or Straight"
        elif (bust - hips) >= 12.7 and (bust - hips) < 38.1 and (bust - waist) >= 17.78:
            return "Inverted Triangle"
    elif gender.lower() == 'women':
        if (bust - hips) > 2.54 and (bust - hips) < 25.4 and (bust - high_hip) >= 22.86:
            return "Top Hourglass"
        elif (hips - bust) >= 9.14 and (hips - bust) < 25.4 and (hips - waist) >= 22.86 and (high_hip - waist) < 12.19:
            return "Bottom Hourglass"
        elif (hips - bust) >= 9.14 and (hips - bust) < 25.4 and (hips - waist) < 22.86 and (hips - waist) >= 9.14:
            return "Triangle or Pear"
        elif (hips - bust) < 9.14 and (bust - hips) < 9.14 and (bust - waist) < 22.86 and (hips - waist) < 25.4:
            return "Rectangle or Banana or Straight"
        elif (bust - hips) >= 9.14 and (bust - waist) < 22.86:
            return "Inverted Triangle"
        elif (hips - bust) >= 9.14 and (hips - waist) < 22.86:
            return "Apple or Round"

# Example usage
body_shape = classify_body_shape('women', 96, 76, 99, 105)
print(body_shape)