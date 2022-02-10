import re
import sys

country_code = r'(?:(?:\+?(?:[0-9])|(?:\([0-9]\)))(?:[- \.\n])?)'  # optional
area_code = r'(?:(?:(?:\([0-9]{3}\))|(?:[0-9]{3}))(?:[- \.\n])?)'  # optional
phone_number1 = r'(?:(?:[0-9]{3})(?:[- \.\n])?)'
phone_number2 = r'(?:[0-9]{4})'

with_country_code = r'(?:^|[^0-9])'+country_code+area_code+phone_number1+phone_number2
with_area_code = r'(?:^|[ \n])'+area_code+phone_number1+phone_number2
no_code = r'(?:^|[ \n])'+phone_number1+phone_number2
final = with_country_code + r'|' + with_area_code+r'|'+ no_code

#print(final)

def tel_match(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        file_str = f.read()
    out_file = 'telephone_output.txt'
    all_digit_match = re.findall(final, file_str)
    #print(all_digit_match)
    with open(out_file, 'w') as f:
        for match in all_digit_match:
            if match[0] == '\n':
                match = match.replace('\n', '', 1)
            elif match[0] == ' ':
                match = match.replace(' ', '', 1)
            match = match.replace('\n', ' ')
            if len(match) == 0:
                continue
            if match[-1] == ' ':
                match = match[0:-1]
            f.write(match + '\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('invalid input, please input only the input file')
    file_path = sys.argv[1]
    tel_match(file_path)