
import sys,os


old__content = sys.argv[1]
new_content = sys.argv[2]
old_name = sys.argv[3]
new_name = sys.argv[4]



if len(sys.argv) ==3:
    f = open(old_name,'r',encoding='utf-8')
    f.close()
    for line in f:
        line = line.replace(old__content,new_content)
    f = open(old_name,'w',encoding='utf-8')
    f.writelines(line)
elif len(sys.argv) ==4:
    f = open(old_name, 'r', encoding='utf-8')
    f_new = open(new_name, 'w+', encoding='utf-8')
    for line in f:
        line = line.replace(old__content, new_content)
    f_new.writelines(line)
else:
    print('the script format should be as below:')
    print('sed.py old_content new_content old_filename [new_filename]')

