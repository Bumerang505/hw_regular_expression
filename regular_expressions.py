import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

new_table = []

pattern = r'(8|\+7)\s*\(?(\d{3})\)?\s*-?(\d{3})-?(\d{2})-?(\d{2})(?:\s*\(?(доб\.)?\s*(\d{3,4})\)?)?'
replacement = r'+7(\2)\3-\4-\5 \6\7'


def separate_names():
    new_table.append(contacts_list[0])
    for i in contacts_list[1:]:
        one_person_row = []
        names = ' '.join(i[:3])
        names_split = names.split()
        for name in names_split:
            one_person_row.append(name)
        new_table.append(one_person_row)
        for n in i[3:]:
            one_person_row.append(n)


separate_names()


header = new_table[0]
merged_data = {}

for entry in new_table[1:]:
    lastname, firstname = entry[0], entry[1]
    key = (lastname, firstname)

    if key not in merged_data:
        merged_data[key] = entry
    else:
        for i in range(2, len(header)):
            if i < len(entry):
                current_value = entry[i]
            else:
                current_value = ""

            if i < len(merged_data[key]):
                existing_value = merged_data[key][i]
            else:
                existing_value = ""

            if current_value and current_value not in existing_value:
                if existing_value:
                    merged_data[key][i] = f"{existing_value}; {current_value}"
                else:
                    merged_data[key][i] = current_value

result = [header]

for key, entry in merged_data.items():
    while len(entry) < len(header):
        entry.append('')
    result.append(entry)


string_info = ''
for i in result:
    done = ', '.join(i)
    string_info += f'{done}\n'

replace_table = re.sub(pattern, replacement, string_info)
rows = replace_table.strip().split('\n')
new_list_for_write = [row.split(', ') for row in rows]

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(new_list_for_write)
