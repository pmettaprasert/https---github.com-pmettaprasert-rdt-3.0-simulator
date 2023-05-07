def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """

    # take the packet and make it even because we need to add it as 16 bit
    # segments. If we have 31 bytes, since each byte is 8 bits, we need to
    # make it 32 bytes so that we can add it as 16 bit segments
    if len(packet_wo_checksum) % 2 == 1:
        packet_wo_checksum += b'\x00'

    # add each 16 bit segment together
    checksum = 0
    for i in range(0, len(packet_wo_checksum), 2):
        checksum += int.from_bytes(packet_wo_checksum[i:i + 2], byteorder='big')

        # account for overflow
        if checksum > 0xffff:
            # wrap around
            checksum = (checksum & 0xffff) + 1

    # calculate the complement
    checksum = ~checksum & 0xffff

    # return the checksum in bytes
    return checksum


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """

    # verify the checksum according to the book, should add up to be 0xffff
    checksum = 0
    for i in range(0, len(packet), 2):
        checksum += int.from_bytes(packet[i:i + 2], byteorder='big')

        # account for overflow
        if checksum > 0xffff:
            # wrap around
            checksum = (checksum & 0xffff) + 1

    # return true if the checksum is 0xffff
    return checksum == 0xffff


def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """

    packet = bytearray()

    packet += b'COMPNETW'

    # leave two bytes for the checksum
    packet += b'\x00\x00'

    # calculate the length of the data and add the ack and seq_num
    length_ack_seq_segment = len(data_str) + 12
    length_ack_seq_segment <<= 1
    length_ack_seq_segment |= ack_num
    length_ack_seq_segment <<= 1
    length_ack_seq_segment |= seq_num

    # add the length, ack, and seq_num to the packet
    packet += length_ack_seq_segment.to_bytes(2, byteorder='big')

    # add the data to the packet
    packet += data_str.encode()

    # calculate the checksum and add it to the packet
    checksum = create_checksum(packet)
    packet[8:10] = checksum.to_bytes(2, byteorder='big')

    return bytes(packet)


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######


def get_seq_num(packet):
    length_ack_seq_segment = int.from_bytes(packet[10:12], byteorder='big')
    seq_num = length_ack_seq_segment & 1
    return seq_num


def get_ack_num(packet):
    length_ack_seq_segment = int.from_bytes(packet[10:12], byteorder='big')
    ack_num = (length_ack_seq_segment >> 1) & 1
    return ack_num
