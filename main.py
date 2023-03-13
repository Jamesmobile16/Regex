import re
from pprint import pprint
import csv

f = "phonebook_raw.csv"
pattern_phone = r"(\+?\d{1})\s*(\(?)(\d{3})(\)?)(\s*|-*)(\d{3})(-*)(\d{2})(-*)(\d{2})"
pattern_add_phone = r"доб.\s*(\d{4})"
substitution = r"+7(\3)\6-\8-\10"
sub_add_phone = r"доб.\1"


def right_phone(person_list, pattern_ph, pattern_add_ph, sub_ph, sub_add_ph):
    add_phone_correct = ''
    phone_correct = ''
    raw_phone = person_list[5]
    if re.search(pattern_ph, raw_phone) is not None:
        phone = re.search(pattern_ph, raw_phone).group()
        phone_correct = re.sub(pattern_ph, sub_ph, phone)
        if re.search(pattern_add_ph, raw_phone) is not None:
            add_phone = re.search(pattern_add_ph, raw_phone).group()
            add_phone_correct = re.sub(pattern_add_ph, sub_add_ph, add_phone)
    if phone_correct:
        phone = phone_correct + ' ' + add_phone_correct
        return phone

def file_opener(file):
    with open(file, encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list

def phonebook(file_name, pattern_ph, pattern_add_ph, sub_ph, sub_add_ph):
    raw_contact_list = file_opener(file_name)
    name_check_dict = {}
    correct_list = []
    for person in raw_contact_list:
        correct_dict = {}
        correct_dict['name'] = (person[0] + ' ' + person[1] + ' ' + person[2]).rstrip()
        check_name_list = correct_dict['name'].split()
        check_name = check_name_list[0] + ' ' + check_name_list[1]
        correct_dict['organization'] = person[3]
        correct_dict['position'] = person[4]
        correct_dict['email'] = person[6]
        correct_dict['phone'] = right_phone(person, pattern_ph, pattern_add_ph, sub_ph, sub_add_ph)
        if check_name not in name_check_dict.keys():
            name_check_dict[check_name] = correct_dict
        else:
            if person[3]:
                name_check_dict[check_name]['organization'] = person[3]
            if person[4]:
                name_check_dict[check_name]['position'] = person[4]
            if person[6]:
                name_check_dict[check_name]['email'] = person[6]
    for value in name_check_dict.values():
        one_person_list = [
            value['name'],
            value['organization'],
            value['position'],
            value['email'],
            value['phone']
        ]
        correct_list.append(one_person_list)
    return correct_list

def writer_file():
    with open("phonebook.csv", "w") as file:
      datawriter = csv.writer(file, delimiter=',')
      # Вместо contacts_list подставьте свой список
      datawriter.writerows(phonebook(f, pattern_phone, pattern_add_phone, substitution, sub_add_phone))


if __name__ == '__main__':
    # pprint(phonebook(f, pattern_phone, pattern_add_phone, substitution, sub_add_phone))
    writer_file()
