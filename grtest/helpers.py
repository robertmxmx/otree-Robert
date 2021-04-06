import csv

def parsecsv(csvfile):
    csvdata = {}
    playerid = 0

    with open(csvfile) as f:
        for line in csv.reader(f):
            batchno = line[0]

            if batchno not in csvdata:
                csvdata[batchno] = []

            csvdata[batchno].append({
                'id': playerid,
                'birth_region': line[1],
                'pol_ideology': line[2]
            })

            playerid += 1

    return list(csvdata.values())

def printxyz(groups):
    x = 0
    y = 0
    z = 0

    for g in groups:
        if g[0]['sorted_by'] == 'birth_region':
            x += 1
        elif g[0]['sorted_by'] == 'pol_ideology':
            y += 1
        else:
            z += 1

    print('(%d, %d, %d)' % (x, y, z))