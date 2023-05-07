from socket import *
from util import *


class Sender:
    def __init__(self):
        """
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()

        Please check the main.py for a reference of how your function will be called.
        """
        print("This is the Sender class.\n")
        print("Run the receiver.py first before running this file.\nThe port "
              "number inputted in the receiver.py will be used here to send "
              "packet to the receiver.\n")

        #create a socket
        self.sock = socket(AF_INET, SOCK_DGRAM)

        #set the timeout to 3 seconds
        self.sock.settimeout(3)

        #ask for ip address
        self.ip_address = input("Enter the ip address of the receiver: ")

        #prompt the user for the port number
        self.port_no = int(input("Enter the port number of the receiver: "))

        self.seq_num = 0


    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

        Args:
          app_msg_str: the message string (to be put in the data field of the packet)

        """

        #Original message string
        print("Original message string: " + app_msg_str)

        #create a packet use the util
        packet = make_packet(app_msg_str, 0, self.seq_num)

        #print the packet
        print("Packet sent: " + str(packet))

        #send the packet
        self.sock.sendto(packet, (self.ip_address, self.port_no))

        #wait for the ack, need to verify the checksum and whether is ack,
        #if not ack, resend the packet
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)

                if not verify_checksum(data) or not get_ack_num(data) == self.seq_num:
                    print("Packet corrupted, waiting for timeout")
                    continue

            except:
                print("Reached end of timeout, resending packet...")
                self.sock.sendto(packet, (self.ip_address, self.port_no))

            else:

                print("Ack received, changing sequence number")
                self.seq_num ^= 1


    ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
    ####### function, which will be called by an application to                 #######
    ####### send a message. DO NOT change the function name.                    #######
    ####### You can have other functions if needed.