import unittest
from util import *

class TestUtil(unittest.TestCase):


    def test_msg1(self):
        msg = "msg1"
        ack = 0
        seq = 0
        packet = make_packet(msg, 0, seq)
        self.assertEqual(packet, b'COMPNETW\xf7\xde\x00@msg1')
        self.assertEqual(get_seq_num(packet), 0)
        self.assertEqual(verify_checksum(packet), True)

    def test_msg2(self):
        msg = "msg2"
        seq = 1
        packet = make_packet(msg, 0, seq)
        self.assertEqual(packet, b'COMPNETW\xf7\xdc\x00Amsg2')
        self.assertEqual(get_seq_num(packet), 1)
        self.assertEqual(verify_checksum(packet), True)

    def test_msg3(self):
        msg = "msg3"
        seq = 0
        packet = make_packet(msg, 0, seq)
        self.assertEqual(packet, b'COMPNETW\xf7\xdc\x00@msg3')
        self.assertEqual(get_seq_num(packet), 0)

        self.assertEqual(verify_checksum(packet), True)

    def test_msg4(self):
        msg = "msg4"
        seq = 1
        packet = make_packet(msg, 0, seq)
        self.assertEqual(packet, b'COMPNETW\xf7\xda\x00Amsg4')
        self.assertEqual(get_seq_num(packet), 1)
        self.assertEqual(verify_checksum(packet), True)

    def test_msg5(self):
        msg = "msg5"
        seq = 0
        packet = make_packet(msg, 0, seq)
        self.assertEqual(packet, b'COMPNETW\xf7\xda\x00@msg5')
        self.assertEqual(get_seq_num(packet), 0)
        self.assertEqual(verify_checksum(packet), True)

    def test_msg6(self):
        msg = "msg6"
        seq = 1
        packet = make_packet(msg, 0, seq)
        self.assertEqual(packet, b'COMPNETW\xf7\xd8\x00Amsg6')
        self.assertEqual(get_seq_num(packet), 1)
        self.assertEqual(verify_checksum(packet), True)

    def test_msg7(self):
        msg = "msg7"
        seq = 0
        packet = make_packet(msg, 0, seq)
        self.assertEqual(packet, b'COMPNETW\xf7\xd8\x00@msg7')
        self.assertEqual(get_seq_num(packet), 0)
        self.assertEqual(verify_checksum(packet), True)
