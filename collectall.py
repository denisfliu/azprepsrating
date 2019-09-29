#!/usr/bin/env python
import preps

if __name__ == '__main__':
    print('Enter teams url: ')
    teamsurl = input()
    with open("data.csv", 'w') as csvfile:
        preps.add_all(teamsurl, csvfile)