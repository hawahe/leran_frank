path = 'C:\\Users\zhao\Desktop\python\Walden1.txt'
with open(path,'r',encoding='UTF-8') as text:
    words = text.read().split()
    print(words)
    #for word in words:
     #   print('{}-{} times'.format(word,words.count(word)))