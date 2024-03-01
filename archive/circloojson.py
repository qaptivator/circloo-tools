import json
def print_dict(d):
    print(json.dumps(d, sort_keys=True, indent=4))

def parseold(s):
    lines = s.split("\n")[3:] # first 3 lines are useless
    res = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(' ')

        if line.startswith('/'):
            parts = parts[1:]

        res.append({
            "key": parts[0],
            "args": parts[1:],
        })
    return res  

def getArgs(line): # get arguments from line
    if line.startswith('/'):
        line = line[2:]
    return line.split(' ')

def toObject(s): # turn string into an object
    lines = s.strip().split("\n")[3:] # first 3 lines are useless
    temp_object = {
        "type": '',
        "props": [],
        "id": 0
    }
    res = {
        "headers": {},
        "objects": [],
    }

    # get the headers (first 8 lines)
    for header in lines[:8]:
        header = header.strip()
        if not header: 
            continue
    
        args = getArgs(header)
        res["headers"][args[0]] = args[1:]
        #res["headers"].append(getArgs(header))

    lines = lines[8:] # we dont need those headers anymore

    # get the objects
    for object in lines:
        object = object.strip()
        if not object: 
            continue

        args = getArgs(object)
        values = [str(x) for x in args[1:]]
        print(args)

        if object.startswith('<'):
            temp_object["id"] = int(args[1])
        elif object.startswith('ic') or object.startswith('c') or object.startswith('b') or object.startswith('l_at') or object.startswith('tmb'):
            temp_object = {
                "type": args[0],
                "props": values
            }
            #temp_object["type"] = args[0]
            #temp_object["props"] = values
            res["objects"].append(temp_object)
            #print(temp_object)

    return res

def parse(s): # parse the string into a level class for further editing
    level = toObject(s)
    return level


level = """/
/ circloO level
/ Made with circloO Level Editor v1.3
totalCircles 4 0
/ EDITOR_TOOL 1 
/ EDITOR_VIEW 2156.50 1833 0.80
/ EDT 4964
/ _SAVE_TIME_1708642659000_END
levelscriptVersion 5
COLORS 213
grav 1 270
y 1425 1560  1 1 1
bullet
< 0
ic 'i' 1655 1557 1 
< 1
l_at 1271 1721 1494 1911 2
< 2
ic 'i' 1294 1798 1 
< 3
c 1273.50 1726 11.945219039916992
< 4
/ LE_ARC_DESCRIPTION 1275.55 1892.66 45.76 236.31 118.18 2164 2373 2 2
/ SKIP 7
* 1
+ -224.45 392.66
repeatchp 45.76 81.82 84 -2
+* 0
chp 236.31 81.82
chmake_arc 0 2
=
< 5
mc 1273.50 1990.50 10.124228477478027 1 0
< 6
ic 'io' 1385 2063 1 
< 7
t 1719 2182 1400 2307 1677 2312
< 8
c 1772.50 2246.50 54.268043518066406
< 9
c 1861.50 2225 40.115459442138672
< 10
ic 'i' 1901 2146 1 
< 11
c 1109 1324 148.600128173828125
< 12
b 1640.50 1110 258.50 72 0
< 13
tmb 1908 1366 179 58 1 -1 0 -1 300 60 0
< 14"""

print_dict(parse(level))