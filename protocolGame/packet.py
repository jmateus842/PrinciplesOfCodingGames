import random
import ipaddress

class Packet:
    def __init__(self, ip_address, description, protocol, is_blacklisted):
        self.ip_address = ip_address
        self.description = description
        self.protocol = protocol
        self.is_blacklisted = is_blacklisted

    @staticmethod
    def generate_random_packet(blacklist):
        is_blacklisted = random.random() < 0.3  # 30% chance of being blacklisted
        
        descriptions = {
            'TCP': [
                'VIP package',
                'Secure file transfer',
                'Database query'
            ],
            'UDP': [
                'Online gaming',
                'Video streaming',
                'Voice chat'
            ],
        }
        protocol = random.choice(['TCP', 'UDP'])
        description = random.choice(descriptions[protocol])

        if is_blacklisted:
            ip_address = random.choice(list(blacklist))
        else:
            while True:
                ip_address = str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
                if ip_address not in blacklist:
                    break

        return Packet(ip_address, description, protocol, is_blacklisted)

    def __str__(self):
        return f"IP: {self.ip_address}, Description: {self.description}, Protocol: {self.protocol}, Blacklisted: {self.is_blacklisted}"
