
import argparse
import sys
import re

dictofstr = {}


def after_context(lines, params, strnumb, grepstr):
    patternstr = params.pattern.replace("*", ".*")
    patternstr = patternstr.replace("?", ".")
    for i,line in enumerate(lines):
        line = line.rstrip()
        if (re.search(patternstr, line)):
            if (line):
                dictofstr.update({i:line})
            if ((len(lines) - i) > abs(strnumb)):
                afterlines = lines[i + 1:][:abs(strnumb)]
                for j,afterline in enumerate(afterlines):
                    dictofstr.update({(i + 1 + j):afterline})
            else:
                afterlines = lines[i + 1:]
                for j,afterline in enumerate(afterlines):
                    dictofstr.update({(i + 1 + j):afterline})


def before_context(lines, params, strnumb, grepstr):
    patternstr = params.pattern.replace("*", ".*")
    patternstr = patternstr.replace("?", ".")
    for i,line in enumerate(lines):
        line = line.rstrip()
        if (re.search(patternstr, line)):
            if (i > abs(strnumb)):
                beforelines = lines[:i][- abs(strnumb):]
                for j,beforeline in enumerate(beforelines[::-1],1):
                    dictofstr.update({(i - j) : beforeline})
            else:
                beforelines = lines[:i]
                for j,beforeline in enumerate(beforelines[::-1],1):
                    dictofstr.update({(i - j):beforeline})
            if (grepstr):
                dictofstr.update({i:line})


def base_context(lines, params):
	before_context(lines, params, params.context, True);
	after_context(lines, params, params.context, False);		


def pattern (lines, params):
    patternstr = params.pattern.replace("*",".*")
    patternstr = patternstr.replace("?",".")
    for i,line in enumerate(lines):
        line = line.rstrip()
        if (re.search(patternstr,line)):
            dictofstr.update({i: line})


def output(line):
    print(line)


def line_number(lines, params, flag):
    patternstr = params.pattern.replace("*", ".*")
    patternstr = patternstr.replace("?", ".")
    for i, line in enumerate(lines, 1):
        line = line.rstrip()
        if (re.search(patternstr, line)):
            output(f'{i}:{line}')
        elif(flag):
            output(f'{i}-{line}')


def count(lines, params):
	counter = 0
	for line in lines:
		line = line.rstrip()
		if params.pattern in line:
			counter += 1
	output(str(counter))


def ignore_case(lines, params):
	for i,line in enumerate(lines):
		line = line.rstrip()
		if params.pattern.lower() in line.lower():
			dictofstr.update({i:line}) 


def invert(lines, params):
	for i,line in enumerate(lines):
		line = line.rstrip()
		if params.pattern not in line:
			dictofstr.update({i:line}) 


def grep(lines, params):
    if (params.invert):
      	invert(lines, params)
    if (params.ignore_case):
     	ignore_case(lines, params)
    if (params.after_context):
        after_context(lines, params, params.after_context, True)
    if (params.before_context):
       	before_context(lines, params, params.before_context, True)
    if (params.context):
    	base_context(lines, params)
    if (params.line_number):
        if (len(list(dictofstr.values())) != 0):
            line_number(list(dictofstr.values()), params, True)
            dictofstr.clear()
        else:
            line_number(lines, params, False)
    if (params.count):
            count(lines, params)
    if ((params.invert == False) and (params.ignore_case == False) and (params.after_context == 0) and (params.before_context == 0)
    and (params.context == 0) and (params.line_number == False) and (params.count == False)):
        pattern(lines, params)


    if(len(dictofstr)):
    	for k in sorted(dictofstr):
    		output(dictofstr[k])
    	dictofstr.clear()


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    #grep(sys.stdin.readlines(), params)
    print(params.after_context)

if __name__ == '__main__':
    main()
