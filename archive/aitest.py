def parse_level(level_text):
    level_lines = level_text.split("\n")
    
    level_data = {}
    objects = []
    
    level_properties = None
    object_properties = None
    
    for line in level_lines:
        line = line.strip()
        
        if not line: 
            continue

        if line.startswith('/'):
            parts = line.split(' ', 2)

            if len(parts) < 2:
                continue

            key = parts[1]
            if len(parts) > 2:
                value = parts[2]
            else:
                value = ''

            if key.startswith('_') and key.endswith('_END'):
                level_data[key] = value #int(value)
            else:
                level_data[key] = value
            
            level_properties = None 
            object_properties = None 
           
        elif line.startswith('COLORS') or line.startswith('grav') or line.startswith('y'):
            parts = line.split(' ')
            key = parts[0]
            destination = level_data

            if key == 'bullet':
                break
            else:
                value = [x for x in parts[1:]]
                destination[key] = value
            
        elif line.startswith('ic') or line.startswith('c') or line.startswith('b') or line.startswith('l_at') or line.startswith('tmb'):
            parts = line.split(' ')
            object_type = parts[0]
            values = [str(x) for x in parts[1:]]
            object_properties = {
                "type": object_type,
                "properties": values
            }
            
            objects.append(object_properties)
            
        elif line.startswith('<'):
            object_properties["id"] = int(line[1:])
            
        elif line.startswith('='):
            break
    
    return level_data, objects


level_text = """/
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
level_data, objects = parse_level(level_text)

print("------------ Level data")
for data in level_data:
    print(data)

print("------------ Objects")
for obj in objects:
    print(obj)