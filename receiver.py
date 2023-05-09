from socket import *
from time import sleep
from util import *


## No other imports allowed.


class Receiver:
    """
    A class that receives packets over a network to simulate rdt3.0. Every
    packet number divisible by 6 will simulate a timeout. If any packet
    number is divisible by 3 after checking 6 first, the receiver will
    simulate a corrupt packet by sending an incorrect ACK. Otherwise the
    receiver will send the correct ACK back to the sender.

    Attributes:
        - port_no (int): the port number to listen on
        - sock (socket): the socket object for sending and receiving data
        - timeout (int): the number of seconds to wait for a packet before
        timing out
        - seq_num (int): the sequence number of the expected packet
        - ack (int): the ack number of the expected packet
        - packet_num (int): the number of packets received so far.


    """

    def __init__(self):
        """
        Initializes the Receiver object.
        """

        print("Receiver class initialized.\n")

        # Ask the user for the port number to bind the socket to.
        self.port_no = int(input("Enter the port number: "))
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.bind(self.port_no)

        # Set the timeout to 40 seconds
        self.timeout = 40
        self.sock.settimeout(self.timeout)
        self.seq_num = 0
        self.ack = 0
        # The number of packets that has arrived.
        self.packet_num = 1
        self.rdt_rcv()

    def bind(self, port_no):
        """
        Binds the socket to a port number. If the port number is in use,
        increment it linearly until it can bind correctly.

        Args:
            port_no (int): the port number to bind the socket to.

        """

        # Try linear probing until the socket is binded to a port number.
        while True:
            try:
                self.sock.bind(('', port_no))
            except:
                port_no += 1
            else:
                break

        # Sets to the new port number.
        self.port_no = port_no

    def rdt_rcv(self):

        """
        Receives packets from the sender. Handles the packet in various ways
        to simulate a rdt3.0.
        """

        print("Receiver will now be listening for packets on\nIP address: " +
              str(gethostbyname(gethostname())) + "\nPort number: " +
              str(self.port_no) + "\nTimeout before closing socket: " + str(
            self.timeout) +
              " seconds\n")

        print("Waiting for packets...\n")

        # Start receiving packets here.
        while True:

            # If the packet is not received in the timeout period, close the
            # socket and exit the program.
            try:

                # Receive the packet and print it out.
                data, addr = self.sock.recvfrom(1024)
                print("Packet " + str(self.packet_num) + " received: " + str(
                    data))

                # Check the checksum of the packet.
                if verify_checksum(data):

                    # if it divisible by 6, simulate timeout
                    if self.packet_num % 6 == 0:
                        print("This packet is divisible by 6. Simulating a "
                              "timeout.\nThe ack for this packet will be "
                              "not be sent back.\n")
                        sleep(6)
                        continue

                    # if it is divisible by 3, simulate packet corruption by
                    # sending the old ack.
                    elif self.packet_num % 3 == 0:
                        print("This packet is divisible by 3. Simulating a "
                              "packet corruption.\nSending back the ack for "
                              "the previous packet.")

                        packet = make_packet('', self.ack, self.seq_num)

                        self.sock.sendto(packet, addr)

                    # if the sequence number is the same as the expected
                    elif get_seq_num(data) == self.seq_num:
                        print(
                            "Packet is expected, messsage string delivered: " +
                            self.get_msg(data))

                        self.ack = self.seq_num

                        print("Sending back the ack for this packet.")

                        packet = make_packet('', self.ack, self.seq_num)

                        self.sock.sendto(packet, addr)
                        self.seq_num ^= 1


                    else:
                        # if all else fails, send back the ack for the previous
                        # packet
                        print("Incorrect sequence number. Sending back the "
                              "ack for the previous packet.")
                        packet = make_packet('', self.ack, self.seq_num)
                        print("Packet sent: " + str(packet))
                        self.sock.sendto(packet, addr)

                print("All done for this packet.\n\n")
                self.packet_num += 1

            # Breaks the loop once the timeout has been reached.
            except:
                break

        # Once the timeout has been reached, close the socket.
        print("Receiver timeout has occurred. Closing the socket.\n")
        self.sock.close()

    def get_msg(self, data):
        """
        Gets the message from the packet.

        Args:
            - data (bytes): the packet to get the message from.

        Returns:
            - str: the message from the packet.
        """
        return str(data[12:].decode('utf-8'))


if __name__ == "__main__":
    # Printing the instructions.
    print("This is the receiver class. Start this file first.\nNO NEED TO ADD"
          " ANY COMMAND LINE ARGS.\n")
    print("The receiver class will ask for a port number so that\n"
          "it can bind to that port and wait for packets.\n")
    print(
        "Once the receiver class receives a packet, it will check for the\nfor"
        "checksum. If the checksum is correct, it will check for these "
        "scenarios:\n")
    print("1. If the packet is divisible by 6, it will simulate a timeout.")
    print("2. If the packet is divisible by 3 (but divisible by 6 is checked "
          "first),\nit will simulate a packet corruption.")
    print("3. If the packet is the expected packet, it will send back the ack "
          "for that packet.")
    print("4. If the packet is not the expected packet, it will send back the "
          "ack for the previous packet.\n")
    print("The receiver class will continue to receive packets until a timeout"
          " occurs\nwhich will close the socket automatically.\n")

    # Creating the Receiver.
    receiver = Receiver()
