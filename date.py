#!/usr/bin/env python
import preps

if __name__ == '__main__':
    print('Enter url: ')
    schoolrosterurl = input()
    with open("data.csv", 'a') as csvfile:
        csvfile.write('\n')
        preps.date_collect(schoolrosterurl, csvfile)