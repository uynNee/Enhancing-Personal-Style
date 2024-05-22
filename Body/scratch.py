import requests
import time
import csv
import os
import concurrent.futures

def send_request_threaded(gender, chest, waist, high, hip):
    # Wrap the send_request function with a try-except block to handle exceptions in threads
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
    
    if shape != "":
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

    genders = ["men", "women"]
    measurement_range = range(21, 51)  # Adjusted range
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for waist in measurement_range:
            for high in measurement_range:
                for hip in measurement_range:
                    for chest in measurement_range:
                        for gender in genders:
                            # Check if the combination already exists in the CSV
                            if not combination_exists(gender, chest, waist, high, hip):
                                send_request(gender, chest, waist, high, hip)
                                time.sleep(0.5)

def combination_exists(gender, chest, waist, high, hip):
    # Check if the combination exists in the CSV file
    with open('scratched_data.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == gender and int(row[1]) == chest and int(row[2]) == waist and int(row[3]) == high and int(row[4]) == hip:
                return True
    return False


if __name__ == "__main__":
    main()