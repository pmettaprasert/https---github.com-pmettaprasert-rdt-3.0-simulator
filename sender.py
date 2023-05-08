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
              "number inputted in the receiver.py will be used\nhere to send "
              "packet to the receiver.\n")

        #create a socket
        self.sock = socket(AF_INET, SOCK_DGRAM)

        #set the timeout to 3 seconds
        self.sock.settimeout(3)

        #ask for ip address
        self.ip_address = input("Enter the ip address of the receiver: ")

        self.ip_address = self.ip_address.strip()

        #prompt the user for the port number
        self.port_no = int(input("Enter the port number of the receiver: "))

        self.seq_num = 0

        self.packet_counter = 1


    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

        Args:
          app_msg_str: the message string (to be put in the data field of the packet)

        """

        #Original message string
        print("\nOriginal message string: \"" + app_msg_str + "\"")

        #create a packet use the util
        packet = make_packet(app_msg_str, 0, self.seq_num)

        #print the packet
        print("Packet sent: " + str(packet) + " with sequence number: " +
              str(self.seq_num))

        #send the packet
        self.sock.sendto(packet, (self.ip_address, self.port_no))

        #wait for the ack, need to verify the checksum and whether is ack,
        #if not ack, resend the packet

        self.received_incorrect_ack = False

        while True:
            try:

                data, addr = self.sock.recvfrom(1024)

                if not verify_checksum(data) or not get_ack_num(data) == self.seq_num:

                    self.received_incorrect_ack = True
                    print("Receiver acked the previous packet, waiting for "
                          "timeout to resend packet...")
                    continue

            except:
                if not self.received_incorrect_ack:
                    print("An ACK has not been received, therefore have "
                          "to wait\nuntil timeout to resend packet...")
                print("Reached end of timeout, resending packet with msg: \"" +
                      app_msg_str + "\"\nand sequence number: " + str(
                    self.seq_num) + "\n\n")


                if self.received_incorrect_ack:
                    print("[ACK-Previous retransmission]: \"" + app_msg_str + "\"")
                else:
                    print("[Timeout retransmission]: \"" + app_msg_str + "\"")

                self.sock.sendto(packet, (self.ip_address, self.port_no))
                self.packet_counter += 1
                continue

            else:

                #print the ack and the sequence number
                print("Packet number " + str(self.packet_counter) + " was "
                        "received correctly.")
                print("Ack number from receiver: " + str(get_ack_num(data)) +
                      " ==\nsequence number from sender: " + str(self.seq_num))

                print("Changing the sequence number from " + str(
                    self.seq_num) + " to " + str(self.seq_num ^ 1))

                self.packet_counter += 1
                self.seq_num ^= 1
                print("All done with this packet.\n\n")
                break



    ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
    ####### function, which will be called by an application to                 #######
    ####### send a message. DO NOT change the function name.                    #######
    ####### You can have other functions if needed.