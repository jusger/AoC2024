

if __name__ == '__main__':
    import re
    import operator
    from functools import reduce

    with open('AoC_Day3.input','r') as infile:
        corrupted_data = infile.read()

    regex = re.compile(r"mul\([0-9]+,[0-9]+\)")
    strip = re.compile(r'[mul\(\)]')
    
    part1answer = reduce(operator.add, [operator.mul(*z) for z in [[int(y) for y in re.sub(strip, '', x).split(',')] for x in re.findall(regex, corrupted_data)]])
    print(f'Part One Answer:\nMultiplied and summed (dot product essentially, could set it up that way): {part1answer}')

    # For part 2, we need to not count valid mul() expressions preceded by a don't() until we see a do() (if it exists)    
    # I'm gonna be clunky because I can't remember exactly how to do the negative / positive lookaheads/behinds (and in python
    # you have to install a different regex than built in to do a variable character lookbehind I think)

    regex2 = re.compile(r"""(don't\(\)|mul\(\d+,\d+\)|do\(\))""")
    cursor = 'do()'
    part2answer = 0
    for x in re.findall(regex2, corrupted_data):
        if x[:3] == 'mul':
            if cursor == 'do()': 
                part2answer += operator.mul(*[int(_) for _ in re.sub(r'[mul\(\)]','', x).split(',')])
        else:
            cursor = x
    print(f'Part Two Answer: Multiplied and summed: {part2answer}')

