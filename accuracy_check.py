# import time

# from categorizer import categorize

# # (description, the category YOU believe is correct)
# EXAMPLES = [
#     ("Swiggy dinner", "Food"),
#     ("Uber to college", "Transport"),
#     ("Netflix", "Entertainment"), 
#     ("Apollo Pharmacy", "Health"),
#     ("Electricity bill", "Bills"),
#     ("Amazon headphones", "Shopping"),
#     ("Udemy course", "Education"),
#     ("Coffee and snacks", "Food"),
#     ("Jio recharge", "Bills"),
#     ("Auto to town", "Transport"),
#     ("Flipkart order for dress", "Shopping"),
#     ("Paracetamol", "Health"),
#     ("Sem fee", "Education"),
#     ("Airtel recharge", "Bills"),
#     ("Church donation","Other"),
#     ("Water Bill","Bills"),
#     ("Loan","Bills"),
#     ("Vehicle Repair","Other"),
#     ("Eye Checkup","Health"),
#     ("Medicine","Bills"),
#     ("Skin care","Shopping"),
#     ("Bus Fare","Transport"),
#     ("Pet Supplies","Other"),
#     ("Circus Ticket","Entertainment"),
#     ("House warming gift","Other"),
#     ("Fresh lime","Food"),
#     ("Fruits and nuts","Food"),
#     ("Book binding","Education"),
#     ("English Class","Education"),
#     ("Shoe","Shopping")
#     # add 23 more of YOUR real expenses here
# ]


# def run():
#     correct = 0
#     failed = 0
#     wrong = []
#     for description, expected in EXAMPLES:
#         predicted = categorize(description)
#         if predicted == "Uncategorized":
#             failed += 1
#         elif predicted == expected:
#             correct += 1
#         else:
#             wrong.append((description, expected, predicted))
#         time.sleep(13)

#     total = len(EXAMPLES)
#     print(f"Correct: {correct}/{total} ({correct / total:.0%})")
#     print(f"Uncategorized (AI call failed): {failed}")
#     for description, expected, predicted in wrong:
#         print(f"WRONG: {description} -> expected {expected}, got {predicted}")


# if __name__ == "__main__":
#     run()   



import json
import os
import time

from categorizer import categorize

RESULTS_FILE = "accuracy_results.json"
MAX_CALLS_PER_RUN = 40 

# (description, the category YOU believe is correct)
EXAMPLES = [
   
    ("Swiggy dinner", "Food"),
    ("Uber to college", "Transport"),
    ("Netflix", "Entertainment"), 
    ("Apollo Pharmacy", "Health"),
    ("Electricity bill", "Bills"),
    ("Amazon headphones", "Shopping"),
    ("Udemy course", "Education"),
    ("Coffee and snacks", "Food"),
    ("Jio recharge", "Bills"),
    ("Auto to town", "Transport"),
    ("Flipkart order for dress", "Shopping"),
    ("Paracetamol", "Health"),
    ("Sem fee", "Education"),
    ("Airtel recharge", "Bills"),
    ("Church donation","Other"),
    ("Water Bill","Bills"),
    ("Loan","Bills"),
    ("Vehicle Repair","Other"),
    ("Eye Checkup","Health"),
    ("Medicine","Bills"),
    ("Skin care","Shopping"),
    ("Bus Fare","Transport"),
    ("Pet Supplies","Other"),
    ("Circus Ticket","Entertainment"),
    ("House warming gift","Other"),
    ("Fresh lime","Food"),
    ("Fruits and nuts","Food"),
    ("Book binding","Education"),
    ("English Class","Education"),
    ("Shoe","Shopping")
    # add 23 more of YOUR real expenses here
]


def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return {}


def save_results(results):
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)


def report(results):
    correct = 0
    wrong = []
    pending = 0
    for description, expected in EXAMPLES:
        if description not in results:
            pending += 1
        elif results[description] == expected:
            correct += 1
        else:
            wrong.append((description, expected, results[description]))

    done = len(EXAMPLES) - pending
    print(f"Done: {done}/{len(EXAMPLES)}  Pending: {pending}")
    if done:
        print(f"Correct: {correct}/{done} ({correct / done:.0%})")
    for description, expected, predicted in wrong:
        print(f"WRONG: {description} -> expected {expected}, got {predicted}")


def run():
    results = load_results()
    calls = 0
    failures = 0
    for description, expected in EXAMPLES:
        if description in results:
            continue
        if calls >= MAX_CALLS_PER_RUN:
            print("Stopping to protect the daily quota. Run again later.")
            break
        predicted = categorize(description)
        calls += 1
        if predicted == "Uncategorized":
            failures += 1
            if failures >= 2:
                print("Two failures in a row: probably out of quota. Stopping.")
                break
        else:
            failures = 0
            results[description] = predicted
            save_results(results)
        time.sleep(13)
    report(results)


if __name__ == "__main__":
    run()