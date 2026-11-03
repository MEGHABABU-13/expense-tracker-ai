from categorizer import categorize

for text in ["Swiggy dinner", "Uber to college", "Netflix", "Apollo Pharmacy", "asdfgh"]:
    print(text, "->", categorize(text))

print("Cached:", categorize("Swiggy dinner"))