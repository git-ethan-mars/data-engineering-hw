with open("third_task_result.txt", "w", encoding="utf-8") as file_output:
    with open("third_task.txt") as file:
        for line in file:
            row = line.split()
            for i in range(len(row)):
                if row[i] == "N/A":
                    row[i] = (row[i - 1] + int(row[i + 1])) / 2
                else:
                    row[i] = int(row[i])
            row = list(filter(lambda x : x % 3 == 0, row))
            row_result = sum(row)
            file_output.write(f"{row_result}\n")
