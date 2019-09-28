#!/usr/bin/env python
import preps

if __name__ == '__main__':
    print('Enter url: ')
    schoolrosterurl = input()
    with open("data.csv", 'w') as csvfile:
        preps.add_info(schoolrosterurl, csvfile)
