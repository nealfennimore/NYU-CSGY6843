from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    myChecksum = 0
    ID = os.getpid() & 0xFFFF  # Return the current process i
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)


    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    packet = header + data
    return packet

def parse_packet(packet):
    names = ["type", "code", "checksum", "packet_id", "seq_number"]
    struct_format = "!BBHHH"
    data = packet[20:28]

    unpacked_data = struct.unpack(struct_format, data)
    return dict(zip(names, unpacked_data))


def get_route(hostname):
    timeLeft = TIMEOUT
    all_traces = [] #This is your list to contain all traces'
    counter = 1

    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            tracelist = [] #This is your list to use when iterating through each trace 

            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)

            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []: # Timeout
                    tracelist.append("* * * Request timed out.")
                    all_traces.append(tracelist)

                recvPacket, addr = mySocket.recvfrom(1024)
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    tracelist.append("* * * Request timed out.")
                    all_traces.append(tracelist)

            except timeout:
                continue

            else:

                packet = parse_packet(recvPacket)

                try: #try to fetch the hostname
                    tracelist.append(addr[0])
                    next_hostname = gethostbyaddr(addr[0])
                    tracelist.append(next_hostname[0])
                except herror:   #if the host does not provide a hostname
                    tracelist.append('hostname not returnable')
                    
                if packet['type'] in [0, 3, 11]:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 +
                    bytes])[0]

                    tracelist.insert(0, f"{timeSent}ms")
                    tracelist.insert(0, f"{counter}")
                    all_traces.append(tracelist)
                    
                    if packet['type'] == 0:
                        return all_traces


                # elif packet['type'] == 3:
                #     bytes = struct.calcsize("d")
                #     timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                #     #Fill in start
                #     #You should add your responses to your lists here 
                #     #Fill in end
                # elif packet['type'] == 0:
                #     bytes = struct.calcsize("d")
                #     timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                #     #Fill in start
                #     #You should add your responses to your lists here and return your list if your destination IP is met
                #     #Fill in end
                else:
                    #Fill in start
                    #If there is an exception/error to your if statements, you should append that to your list here
                    #Fill in end
                    break
            finally:
                mySocket.close()
                counter += 1

if __name__ == '__main__':
    get_route("google.co.il")
