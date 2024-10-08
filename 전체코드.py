#%%
def write_sheet(headers, today, i, start_level, cur, conn):
    print(start_level,"collecting data...")
    statList = []
    index = 0
    count = 1
    level = 300
    weight =  {285:140, 280:12, 275:6, 270:4,260:1}
    weight_i =  {285:1, 280:1, 275:1, 270:1,260:1}
    stat_cut = {285:40000000, 280:30000000, 275: 20000000, 270:10000000,260:5000000}
    while(level > start_level):
        print(count)
        count += 1
        ocidList = []
        nameList = get_name(headers, today, i, weight[start_level])

        for name in nameList:
            ocid = get_ocid(headers, name)
            stat = get_stat(headers, ocid, today)
            if stat != -1 and stat > stat_cut[start_level]:
                statList.append(stat)
        level = get_level(headers, ocid, today)
        i = i+weight_i[start_level]
    sum = 0
    leng = len(statList)

    statList.sort()
    statList.reverse()
    print("size:", leng)
    print(start_level,"writing data...")
    for power in statList:
        if power != -1:
            index += 1
            cur.execute("SELECT stat_detail_%d FROM stat_detail WHERE id = %d;" %(start_level, index))
            result = cur.fetchall()
            try:
                x = result[0]
                cur.execute("UPDATE stat_detail SET stat_detail_%d = %d WHERE id = %d;" 
                            %(start_level, power, index))
            except:
                cur.execute("INSERT INTO stat_detail (id, stat_detail_%d) VALUES(%d, %d);"
                        %(start_level, index, power))
            sum = sum + (power)
    cur.execute("INSERT INTO stat_average (average_stat, leng) VALUES (%d, %d);" %(sum / leng, leng))
    
    conn.commit()
    print(start_level,"end", leng)
    return i