od_do_bool = [1,5,8]
vsetky = []

print(od_do_bool,vsetky)

vsetky.append(od_do_bool[:])
print(od_do_bool,vsetky)
od_do_bool[2] = 10

vsetky.append(od_do_bool[:])
print(od_do_bool,vsetky)
od_do_bool=[0,0,0]
vsetky.append(od_do_bool[:])

print(od_do_bool,vsetky)


