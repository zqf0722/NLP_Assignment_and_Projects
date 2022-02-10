import sys
import re

digit = r'(?:[0-9]+(?:,[0-9]+)*(?:\.[0-9]*)?)'
digit_dollar_regex = r'(?:\$[0-9]+(?:,[0-9]+)*(?:\.[0-9]*)?)(?:(?:(?: |\n)(?:billion|million|trillion))|M)?'
number_in_words = r'(?:(?:hundreds of)+|(?:thousands of)+|(?:half a)|(?:quarter of a)' \
                  r'|a|one|two|three|four|five|six|seven|eight|nine)'
tenth = r'(?:ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty' \
        r'|sixty|seventy|eighty|ninety)'

hundreds = r'(?:' \
          r'(?:one|two|three|four|five|six|seven|eight|nine)' \
          r'(?:(?: |\n)(?:hundred|hundreds))' \
          r'(?:(?: |\n)and(?: |\n)' \
          r'(?:ten|eleven|twelve|thirteen|fourteen|' \
          r'fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|' \
          r'ninety)(?:(?: |\n)(?:one|two|three|four|five|six|seven|eight|nine))?' \
          r')?' \
          r')'
any_number = r'(?:'+number_in_words+r'|' + tenth+r'(?:(?: |\n)'+number_in_words + r')?)'
any_number_smaller_than_thousands = r'(?:'+any_number+r'|'+hundreds+r')'
dollars = r'(?:(?:(?: |\n)[a-zA-Z]*)?(?: |\n)dollars?)'
cents = r'(?:(?: |\n)cents?)'
thousand_times = r'(?:thousands?|millions?|billions?|trillions?)'
number_more_than_thousand = r'(?:'+ any_number_smaller_than_thousands + r'(?:(?: |\n)' + thousand_times\
                            + r'(?: |\n)and(?: |\n)' + any_number_smaller_than_thousands\
                            +r')*'\
                            +r')'
#any_number_smaller_than_thousands = r'(?:' + r'(?:'+any_number_smaller_than_thousands+r'|'+digit +r')'+ dollars + r')'
number_more_than_thousand = r'(?:' + r'(?:'+number_more_than_thousand+r'|'+digit +r')'+ dollars + r')'
number_for_cent = r'(?:'+r'(?:'+any_number+r'|'+digit+r')'+ cents +r')'

#any_number = any_number_smaller_than_thousands + r'(?: |\n)' + thousand_times
final = r'(?:'+r'(?:'+number_more_than_thousand + r'(?:(?: |\n)and(?: |\n)' + \
        number_for_cent+ r')' + r'?' +r')'\
        +r'|' + r'(?:'+ r'(?:'+number_more_than_thousand + r'(?: |\n)and(?: |\n))?' + \
        number_for_cent + r')'+r')'
final = r'(?:'+final + r'|'+digit_dollar_regex+r')'
#any_number = any_number + r'(?:hundred|hundreds)'+ r'(?:(?: |\n)and(?: |\n)' + any_number + r')?'
'''
If you would like to see the final regular expression, you can print final
However, I'm sorry to inform you that it's ugly.

print(final)

It may be more explict to check the component of the final regular expression
I put some of the important regular expression and its meaning down there

digit: The digit might be used in dollar
digit_dollar_regex: All dollars expressed with digit
number_in_words: Simple words/phrases that are used to describe amount
tenth: Expressions for the tenth place
hundreds: Expression for the hundreds
any_number_smaller_than_thousands: The words expression for any number that is less than 1000
It's important because in English, we use 1000 to count. 
dollars, cents: amount
thousand_times: amount greater than 1000 i.e. thousands, million, billion, and etc.
they typically play the same role in describing amount
number_more_than_thousand: Ideally any amount of dollar can be described
number_for_cent: Expressions for cents
final: Combine dollars and cents and together with the digit expression
'''

def dollar_match(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        file_str = f.read()
    out_file = 'dollar_output.txt'
    all_digit_match = re.findall(final, file_str)
    with open(out_file, 'w') as f:
        for match in all_digit_match:
            match = match.replace('\n', ' ')
            f.write(match + '\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('invalid input, please input only the input file')
        exit(0)
    file_path = sys.argv[1]
    dollar_match(file_path)


