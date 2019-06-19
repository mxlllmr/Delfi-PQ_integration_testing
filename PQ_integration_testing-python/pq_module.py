import json
import numpy as np
from datetime import date
from datetime import datetime

def load_json(log_file):
    packets = []
    for line in log_file:
        try:
            packets.append(json.loads(line))
        except:
            break
    return packets

def filter_sbs(packets, sbs):
    res = []
    for packet in packets:
        if packet['Source'] == sbs:
            res.append(packet)
    return res

def filter_param(packets, sbs, param):
    res = []
    dt = []
    for packet in packets:
        if (packet['Source'] == sbs or sbs == 'all') and param in packet:
            res.append(packet[param])
            dt.append(cnv_to_timestamp(packet['_timestamp_']))
    return res, dt

def filter_housekeeping_param(packets, sbs, param):
    res = []
    dt = []
    for packet in packets:
        if (packet['Source'] == sbs or sbs == 'all') and param in packet and packet['Service'] == 'Housekeeping':
            res.append(packet[param])
            dt.append(cnv_to_timestamp(packet['_timestamp_']))

    res = map(float, res)
    return res, dt

def filter_housekeeping_rf_param(packets, sbs_id, param):
    res = []
    dt = []
    for packet in packets:
        if (packet['Source'] == 'OBC') and param in packet and packet['Request'] == 'RF_TX' and packet['SystemID'] == sbs_id:
            res.append(packet[param])
            dt.append(cnv_to_timestamp(packet['_timestamp_']))

    res = map(float, res)
    return res, dt

def find_request_response(packets, sbs, service):
    rq = 0
    rp = 0
    for packet in packets:
        if packet['Destination'] == sbs and packet['Request'] == 'Request' and (packet['Service'] == service or service == 'all'):
            rq += 1
        elif packet['Source'] == sbs and packet['Request'] == 'Reply' and (packet['Service'] == service or service == 'all'):
            rp += 1
    print "Number of requests/responses", rq, "/", rp, "missing", rq - rp, "for", sbs, "and service", service

# def check_hk_rf(packets, sbs):
#     packet_resp = []
#
#     for packet in packets:
#         if packet['Source'] == sbs and packet['Service'] == 'Housekeeping':
#             packet_resp = packet
#
#         elif packet['Source'] == 'OBC' and packet['Request'] == 'RF_TX' and packet_resp['SystemID'] == packet['SystemID']:
#
#     print "Number of requests", rq, "Number of responses", rp, "for", sbs

def cnv_to_timestep_arr(arr):
    dt_list = []
    for i in range(len(arr)):
        if i == 0:
            dt_list.append(0)
        else:
            dt_list.append((arr[i] - arr[0]).total_seconds())
    return dt_list

def cnv_to_timedt_arr(arr):
    dt_list = []
    for i in range(len(arr)):
        if i == 0:
            dt_list.append(0)
        else:
            dt_list.append((arr[i] - arr[i-1]).total_seconds())
    return dt_list

def cnv_to_timestamp_arr(str):
    dt_obj = []
    for st in str:
        dt_obj.append(cnv_to_timestamp(st))
    return dt_obj

def cnv_to_timestamp(str):
    rep = str.replace(' CEST','')
    dt_obj = datetime.strptime(rep, "%a %b %d %H:%M:%S %Y")
    return dt_obj

def find_packets_time_stats(packets, sbs):
    time_list = []
    step_list = []
    dt_list = []

    print "For", sbs

    time_stats, dt = filter_param(packets, sbs, '_timestamp_')

    for obj in time_stats:
        time_list.append(cnv_to_timestamp(obj))

    for i in range(len(time_list)):
        if i == 0:
            step_list.append(0)
            dt_list.append(0)
        else:
            step_list.append((time_list[i] - time_list[0]).total_seconds())
            dt_list.append((time_list[i] - time_list[i-1]).total_seconds())

    print "first packet", time_list[0],"last packet", time_list[-1], "Duration", time_list[-1] - time_list[0], "sec", step_list[-1]

    arr = np.array(dt_list)

    print "packets time average", np.mean(arr), "standard deviation", np.std(arr), "min", np.min(arr), "max", np.max(arr)

def find_rf_packets(packets, sbs, sbs_id):
    rf_packets = 0
    for packet in packets:
        if packet['Request'] == 'RF_TX' and int(packet['SystemID']) == sbs_id:
            rf_packets += 1
    print "RF packets", rf_packets, "in", sbs

def find_boot_counter_resets(packets, sbs, debug):
    prev = 0
    reset = 0

    res, dt = filter_housekeeping_param(packets, sbs, 'BootCounter')

    for i in range(len(res)):
        if i == 0:
            prev = res[i]
        elif prev != res[i]:
            if debug == True:
                print "Reset in:", prev, res[i]
            reset += 1
            prev = res[i]

    print "Resets", reset, "in", sbs

def find_packet_counter_resets(packets, sbs, debug):
    reset = 0
    prv = -1
    for packet in packets:
        if packet['Source'] == sbs:
            if int(packet['Counter']) == 1 and prv != 0 and prv != -1:
                if debug == True:
                    print "Reset in", packet['Counter'], prv
                reset += 1
            prv = int(packet['Counter'])
    print "Resets", reset, "in", sbs

def find_num_packets(packets, sbs):
    num = 0
    if sbs == 'all':
        num = len(packets)
    else:
        res = filter_sbs(packets, sbs)
        num = len(res)
    return num

def find_lost_packets(packets, sbs, debug):
    prv = 0
    lost = 0
    cnt = 0

    for packet in packets:
        if packet['Source'] == sbs:
            if cnt == 0:
                prv = int(packet['Counter'])
            else:
                if int(packet['Counter']) - prv != 1:
                    lost += 1
                    if debug == True:
                        print "lost packet in:", prv, packet['Counter'], packet['_timestamp_']
                prv = int(packet['Counter'])
            cnt += 1

    print "Number of lost packets in", sbs, lost, "/", cnt
