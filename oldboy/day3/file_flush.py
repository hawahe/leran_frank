import sys,time
sys.stdout.write('#')

for i in range(50):
    sys.stdout.write('#')
    sys.stdout.flush()      #内容不用等写入缓冲区后一起输入，而是实时输出在屏幕上，由此实现进度条读取的效果；
    time.sleep(0.1)
