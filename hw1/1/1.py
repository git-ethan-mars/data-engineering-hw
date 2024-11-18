import string
from collections import Counter

vowel_letters = 0
letters = 0
vowel_characters = ["a", "e", "i", "o", "u", "y"]
counter = Counter()
with open("first_task.txt") as file:
    for line in file:
        filtered_line = line.replace("'", "").replace("?", "").replace("!", "").replace(".", "").replace("-", "").replace(",", "").lower()
        words = filtered_line.split()
        counter.update(words)
        for elem in filtered_line:
            if elem in vowel_characters:
                vowel_letters += 1
            if elem in string.ascii_letters:
                letters += 1
with open("first_task_result_1.txt", "w", encoding="utf-8") as file_output:
    for pair in counter.most_common():
        file_output.write(f"{pair[0]}:{pair[1]}\n")
with open("first_task_result_2.txt", "w", encoding="utf-8") as file_output:
    file_output.write(f"{vowel_letters}\n")
    file_output.write(f"{vowel_letters / letters}")
