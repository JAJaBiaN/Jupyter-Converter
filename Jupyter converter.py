import json
import string

print("##Note: Please include file extensions##")

in_file = None
while in_file==None or in_file=='':
    in_file = input("What notebook should be converted? ")

with open(in_file, "r") as f:
    jupy_dict = json.load(f)


def comment_format(line):
    # A line of #'s will be put above and below a h1 or h2 header
    big_header_start = False
    big_header_end = False
    
    # Search for headers in the line
    count_h = line.count('h')
    start = 0
    i=0 # Make sure the loop stops during creation and testing
    while count_h > 0 and i < 100:
        i+=1
        h_index = line.find('h', start)
        if line[h_index - 1] == '<' and line[h_index + 1] in string.digits:
            # Make headings look more obvious by using more #'s
            line_add = '##'
            if int(line[h_index + 1]) <= 2:
                big_header_start = True
                line_add = '####'
            
            label_end = line.find('>', h_index)+1
            line = line.replace(line[h_index-1:label_end], line_add+' ')
            count_h-=1
        elif line[h_index-2:h_index] == '</' and line[h_index + 1] in string.digits:
            # Same again but the else has the line of #'s underneath
            line_add = '##'
            if int(line[h_index + 1]) <= 2:
                big_header_end = True
                line_add = '####'
            
            label_end = line.find('>', h_index)+1
            line = line.replace(line[h_index-2:label_end], ' '+line_add)
            count_h-=1
            
        else:
            start = h_index+1
    
    # Add the line of #'s for big headers
    length = len(line)
    if big_header_start:
        line = '#'*length+'\n'+line
    if big_header_end:
        line = line+'\n'+'#'*length+'\n'
    
    if (not big_header_start) and (not big_header_end):
        line = '##'+line+'##\n'
    
    return line

out_file = None
while out_file==None or out_file=='':
    out_file = input("What should the output sciprt be called?\n"
                     "Enter 'same' to change only the name's extension: ")
    if out_file == 'same':
        out_file = in_file.replace('ipynb', 'py')

with open(out_file, "w") as wf:
    for cell in jupy_dict["cells"]:
            if cell['cell_type']=='code':
                for line in cell['source']:
                    wf.write(line)
                wf.write('\n\n')
            elif cell['cell_type']=='markdown':
                # Add an empty line for emphasis
                wf.write('\n')

                # Write the markdown
                if len(cell['source'])>3:
                    wf.write('"""\n'),
                    for line in cell['source']:
                        wf.write(comment_format(line))
                    wf.write('"""\n')
                else:
                    for line in cell['source']:
                        wf.write(comment_format(line))



