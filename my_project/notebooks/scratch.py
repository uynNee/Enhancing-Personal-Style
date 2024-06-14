import requests
import time
import csv
import os
import concurrent.futures
import pandas as pd

def send_request_threaded(gender, chest, waist, high, hip):
    try:
        send_request(gender, chest, waist, high, hip)
    except Exception as e:
        print(f"Error in thread: {e}")
        
def send_request(gender, chest, waist, high, hip):
    url = "https://calculator-online.net/calculate-with-ajax/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "gender": gender,
        "chest": chest,
        "waist": waist,
        "high": high,
        "hip": hip,
        "unit_s": "imp",
        "cal_url": "body-shape-calculator",
        "cal_cat": "Health",
        "cal_fun": "body_shape",
        "submit": "calculate"
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        response_data = response.json()
        shape = response_data.get("shape", "")
        whr = response_data.get("whr", "")
        status = "succeeded"
    else:
        shape = ""
        whr = ""
        status = "failed"
    
    if shape is not None and shape != '':
    # Write to CSV
        with open('scratched_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([gender, chest, waist, high, hip, shape, whr, status])
        
    print(f"Request {status} for gender: {gender}, chest: {chest}, waist: {waist}, high: {high}, hip: {hip}")

def main():
    # Create CSV file and write headers if it does not exist
    if not os.path.exists('scratched_data.csv'):
        with open('scratched_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Gender", "Chest", "Waist", "High", "Hip", "Shape", "WHR", "Status"])
    else:
        # Read the last row of the CSV file
        last_row = pd.read_csv('scratched_data.csv').iloc[-1]

        # Extract the parameters from the last row
        last_gender = last_row['Gender']
        last_chest = last_row['Chest']
        last_waist = last_row['Waist']
        last_high = last_row['High']
        last_hip = last_row['Hip']

    genders = ["men", "women"]
    measurement_range = range(20, 41)  # Adjusted range

    with concurrent.futures.ThreadPoolExecutor() as executor:
        start = False if os.path.exists('scratched_data.csv') else True
        for waist in measurement_range:
            for high in measurement_range:
                for hip in measurement_range:
                    for chest in measurement_range:
                        for gender in genders:
                            if not start:
                                if gender == last_gender and chest == last_chest and waist == last_waist and high == last_high and hip == last_hip:
                                    start = True
                                continue
                            while True:
                                try:
                                    send_request(gender, chest, waist, high, hip)
                                    break  # If the request is successful, break the loop
                                except Exception as e:
                                        print(f"Error: {e}, retrying in 2 seconds...")
                                        time.sleep(2)  # Wait for 2 seconds before retrying
if __name__ == "__main__":
    main()