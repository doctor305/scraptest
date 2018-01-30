from myLog import MyLog

if __name__ == '__main__':
    m1 = MyLog()
    m1.debug('I am debug message')
    m1.info('I am info message')
    m1.warn('I am warn message')
    m1.error('I am error message')
    m1.critical('I am critical message')

