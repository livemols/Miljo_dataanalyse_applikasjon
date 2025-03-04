file_path = "Oslo-blindern.csv"
with open(file_path, "r") as file:
    for line in file:
        elements = line.strip().split(";")
        fourth_element = elements[3]
        print(fourth_element)