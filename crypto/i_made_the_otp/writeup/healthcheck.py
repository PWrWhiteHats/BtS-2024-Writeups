import struct
import hashlib

java_files = {
    'GeneratePad.java': 'dc5dd43fdb36f7fbe8e562b267d4324fa7e62a381f08fcf2e2eec304ef33ce16',
    'OTPCrypt.java': 'b1252718721a5942ac4afa52c8b8c127817721149224ffd7804ca5d141af14c0'
}
for file, hash_ in java_files.items():
    with open('../challenge/' + file, 'rb') as java_file:

        sha256 = hashlib.sha256()
        sha256.update(java_file.read())
        if sha256.hexdigest() != hash_:
            exit(1)


class JavaCracker:
    a = 0x5DEECE66D
    c = 11
    m = 2 ** 48

    def next_state(self, state):
        return (state * self.a + self.c) % self.m

    def previous_state(self, state):
        s = (state - self.c) % self.m
        return s * pow(self.a, -1, self.m) % self.m

    def get_rand(self, state):
        return state >> 16

    def crack(self, known_numbers: tuple):
        upper_part = known_numbers[0] << 16
        for possible_lower_part in range(0, 2 ** 16):
            possible_state = upper_part + possible_lower_part
            if self.get_rand(self.next_state(possible_state)) == known_numbers[1]:
                primary_seed = self.previous_state(possible_state)
                return primary_seed


with open('../challenge/message.txt', 'rb') as msg_f:
    known_data = msg_f.read()[:8]


with open('../challenge/encrypted.bin', 'rb') as f:
    encrypted_data = f.read()
    key_part = bytes(k ^ e for k, e in zip(known_data, encrypted_data))
    key_part = key_part[:(len(key_part) // 4) * 4]
    known_numbers = []
    for (number,) in struct.iter_unpack('<I', key_part):
        known_numbers.append(number)
    cracker = JavaCracker()
    state = cracker.crack(known_numbers)
    recovered_key = b''
    for i in range(0, len(encrypted_data), 4):
        state = cracker.next_state(state)
        recovered_key += cracker.get_rand(state).to_bytes(4, 'little')

    decrypted_message = ''.join(chr(e ^ k) for e, k in zip(encrypted_data, recovered_key))
    if 'BtSCTF{M4yb3_LCG_i5_n0t_so_raNdom_841f3b4}' in decrypted_message:
        exit(0)
exit(1)
