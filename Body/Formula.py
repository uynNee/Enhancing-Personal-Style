def classify_body_shape(gender, bust, waist, hips, high_hip=None):
    if gender == 'female':
        if (hips - bust) >= 3.6 and (hips - bust) < 10 and (hips - waist) >= 9 and (high_hip is not None and high_hip < 1.193):
            return 'Bottom Hourglass'
        elif (bust - hips) > 1 and (bust - hips) < 10 and (bust - high_hip) >= 9:
            return 'Top Hourglass'
        elif (hips - bust) >= 3.6 and (hips - waist) < 9:
            return 'Triangle or Pear'
        elif (hips - bust) < 3.6 and (bust - hips) < 3.6 and (bust - waist) < 9 and (hips - waist) < 10:
            return 'Rectangle or Banana or Straight'
        elif (bust - hips) >= 3.6 and (bust - waist) < 9:
            return 'Inverted Triangle'
        elif (hips - bust) >= 3.6 and (hips - waist) < 9:
            return 'Apple or Round'
        elif abs(hips - bust) <= 5 and abs(bust - hips) <= 5 and (hips - waist) >= 9:
            return 'Hourglass'
        else:
            return 'Undefined'
    
    elif gender == 'male':
        if (bust - hips) <= 2 and (hips - bust) <= 2 and (bust - waist) >= 5 and (hips - waist) >= 5:
            return 'Bottom Hourglass'
        elif (hips - bust) >= 2 and (waist - bust) < 7:
            return 'Triangle or Pear'
        elif (bust - hips) < 2 and (hips - bust) < 2 and (bust - waist) < 7 and (hips - waist) < 5:
            return 'Rectangle or Banana or Straight'
        elif (bust - hips) >= 5 and (bust - hips) < 15 and (bust - waist) >= 7:
            return 'Inverted Triangle'
        else:
            return 'Undefined'
    
    return 'Undefined'

# Example usage for women
gender = 'female'
bust = 36
waist = 28
hips = 38
high_hip = 37

body_shape = classify_body_shape(gender, bust, waist, hips, high_hip)
print(f"The body shape is: {body_shape}")

# Example usage for men
gender = 'male'
bust = 40
waist = 32
hips = 38

body_shape = classify_body_shape(gender, bust, waist, hips)
print(f"The body shape is: {body_shape}")
