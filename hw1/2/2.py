import math

min_value = float("+inf")
max_value = float("-inf")
with open("second_task_result.txt", "w", encoding="utf-8") as file_output:
    with open("second_task.txt") as file:
        for line in file:
            numbers = [int(s) if int(s) <= 0 else math.sqrt(int(s))  for s in line.split()]
            row = math.modf(sum(numbers))[1]
            if row < min_value:
                min_value = row
            if row > max_value:
                max_value = row
            file_output.write(f"{row}\n")
        file_output.write("\n")
        file_output.write(f"{max_value}\n")
        file_output.write(f"{min_value}\n")

