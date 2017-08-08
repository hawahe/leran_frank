policy_dic = {}
policy_list = []
f1 = open('junos_policy.txt', 'r')
for line in f1:
    i = 4
    while i > 0:

    line_list = line.split()
    if line_list[10] == "source-address":
        policy_dic[line] = policy_list
    else:
        policy_list.append(line)
        else:
            network_list = line_list[-1].split("/")
            ipaddr = network_list[0]
            zone_name = junos_zone_lookup("x.x.x.x", "username", "password", ipaddr)
            line_list[4] = zone_name
            network_obj = " ".join(line_list)
            print(network_obj)
        policy_dic[key] = line

