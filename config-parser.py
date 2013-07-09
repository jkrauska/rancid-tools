#!/usr/bin/python
'''
Simple Cisco Switch Config Parser 

Can be used with rancid configuration collectors.

Aggregates self-similar port configurations to identify irregularities.

'''

import fileinput
import re
descriptionLine=re.compile('^ description')
commentLine=re.compile('^!')
interfaceLine=re.compile('^interface')

interfaceConfigs=False
settingCollect = {}
settingPortCollect = {}

for line in fileinput.input():
    line=line.rstrip()

    if interfaceLine.match(line):
        interfaceConfigs = True
        interfaceName=line.replace('interface ','').replace('GigabitEthernet','Gi')
        interfaceSettings = []
        #print '-'*80

    elif commentLine.match(line) and interfaceConfigs:
        interfaceConfigs = False
        #print 'Settings', interfaceSettings
        foo="\n".join(interfaceSettings)
        try:
            settingCollect[foo] += 1
            settingPortCollect[foo] = settingPortCollect[foo] + ', ' + interfaceName
        except:
            settingCollect[foo] = 1
            settingPortCollect[foo] = interfaceName
        


    
    if interfaceConfigs and \
    not interfaceLine.match(line) and \
    not descriptionLine.match(line):
        
        #print interfaceName, line
        interfaceSettings.append(line)


# After Parsing the File
for setting in settingCollect.keys():
    #print '='*80
    #print 's'
    #print setting
    #print 'sc'
    #print settingCollect[setting]
    #print 'spc'
    #print settingPortCollect[setting]


    print '-' * 80
    print 'Config pattern:'
    print setting
    print 'Count:', len(settingPortCollect[setting].split(','))
    print 'Port List:', settingPortCollect[setting]



