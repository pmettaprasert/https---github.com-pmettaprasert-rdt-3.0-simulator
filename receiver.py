from socket import *
from time import sleep
from util import *


## No other imports allowed


class Receiver:
    def __init__(self):

        print("Receiver class initialized.\n")
        self.port_no = int(input("Enter the port number: "))
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.bind(self.port_no)
        self.timeout = 20
        self.sock.settimeout(self.timeout)
        self.seq_num = 0
        self.packet_num = 1
        self.rdt_rcv()

    def bind(self, port_no):

        # Increment linear probing by 1 if port doesn't work
        while True:
            try:
                self.sock.bind(('', port_no))
            except:
                port_no += 1
            else:
                break

        self.port_no = port_no

    def rdt_rcv(self):

        print("Receiver will now be listening for packets on\nIP address: " +
                str(gethostbyname(gethostname())) + "\nPort number: " +
                str(self.port_no) + "\nTimeout: " + str(self.timeout) +
              " seconds\n")

        print("Waiting for packets...\n")
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                print("Packet " + str(self.packet_num) + " received: " + str(
                    data))

                # check for checksum
                if verify_checksum(data):

                    # if it divisible by 6, simulate timeout
                    if self.packet_num % 6 == 0:
                        time = 4
                        print("This packet is divisible by 6. Simulating a "
                              "timeout.\nThe ack for this packet will be "
                              "delayed by " + str(time) + " seconds.\n")

                        sleep(time)

                    #if it is divisible by 3, simulate packet corruption
                    elif self.packet_num % 3 == 0:
                        print("This packet is divisible by 3. Simulating a "
                              "packet corruption.\nSending back the ack for "
                              "the previous packet.\n")

                        packet = make_packet('', self.seq_num, self.seq_num)
                        print("Packet sent: " + str(packet))
                        print("The ACK for this packet is " + str(self.seq_num))

                        self.sock.sendto(packet, addr)

                    # if the sequence number is the same as the expected
                    elif get_seq_num(data) == self.seq_num:
                        print("Packet is expected, messsage: " +
                              self.get_msg(data))

                        self.ack = self.seq_num

                        print("Sending back the ack for this packet.\n")

                        packet = make_packet('', self.ack, self.seq_num)

                        self.seq_num ^= 1

                    else:
                        #send ack for the previous packet
                        print("Incorrect sequence number. Sending back the "
                              "ack for the previous packet.\n")
                        packet = make_packet('', self.ack, self.seq_num)
                        print("Packet sent: " + str(packet))
                        self.sock.sendto(packet, addr)


            #need to try and see if a timeout occurs it will go into the except
            except:
                break


        print("Receiver timeout has occurred. Closing the socket.\n")
        self.sock.close()







    def get_msg(self, data):
        return str(data[12:])


if __name__ == "__main__":
    print("This is the receiver class. Start this file first.\nNO NEED TO ADD"
          " ANY COMMAND LINE ARGS.\n")
    print("The receiver class will ask for a port number so that\n"
          "it can bind to that port and wait for packets.\n")
    print("Once the receiver class receives a packet, it will check for the\nfor"
            "checksum. If the checksum is correct, it will check for these "
          "scenarios:\n")
    print("1. If the packet is divisible by 6, it will simulate a timeout.")
    print("2. If the packet is divisible by 3 (but divisible by 6 is checked "
          "first), it will simulate a packet corruption.")
    print("3. If the packet is the expected packet, it will send back the ack "
            "for that packet.")
    print("4. If the packet is not the expected packet, it will send back the "
            "ack for the previous packet.\n")
    print("The receiver class will continue to receive packets until a timeout"
            " occurs\nwhich will close the socket automatically.\n")
    receiver = Receiver()
