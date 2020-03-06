#!/usr/bin/env python
import preps

if __name__ == '__main__':
    print('Enter teams url: ')
    teamsurl = input()
    with open("data.csv", 'w') as csvfile:
        preps.get_individuals_schools(teamsurl, csvfile)