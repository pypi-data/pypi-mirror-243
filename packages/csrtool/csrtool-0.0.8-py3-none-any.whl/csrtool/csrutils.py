from typing import List
import sys
import ipaddress
import re

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# typing hint
StrArr = List[str]

valid_rsa_key_sizes = [1024, 2048, 3072, 4096, 8129, 16384]

# match ips in dns-names
ip_exp = re.compile('^ip:', re.I)

def validate_key_size(key_size: int):
    """
    Checks that the RSA key size is one of the allowed values.
    """
    match = valid_rsa_key_sizes.index(key_size)
    if key_size <= 2048:
        print("WARNING: 2048bit keysize is the minimum size that should be used, 4096 recommended", file=sys.stderr)

def generate_private_key(key_size=4096, public_exponent=65537) -> rsa.RSAPrivateKey:
    """
        public_exponent should be 65537 for almost everyone, only in some cases 3 for legacy reasons,
        see: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey
        key_size should be at least 2048, but 1024 is the smallest accepted
    """
    if key_size < 1024:
        raise ValueError("key_size must be at least 1024")

    return rsa.generate_private_key( public_exponent, key_size )

def generate_csr(org: str, ou: str, c: str, dns_names: StrArr, private_key: rsa.RSAPrivateKey) -> x509.CertificateSigningRequest:
    """
    Returns CSR-object based on input. Private key is from method `generate_private_key`
    """

    builder = x509.CertificateSigningRequestBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, dns_names[0]),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ou),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COUNTRY_NAME, c)
    ]))

    # split IP-addresses from DNS-names
    alt_dns_names_without_ip = filter(lambda name: not ip_exp.match(name), dns_names)
    alt_ips = filter(lambda name: ip_exp.match(name), dns_names)

    # add DNSname(s)
    builder = builder.add_extension(
        x509.SubjectAlternativeName(
            list(map(lambda x: x509.DNSName(x), alt_dns_names_without_ip)) + list(map(lambda x: x509.IPAddress(ipaddress.ip_address(x[3:])), alt_ips))
        ),
        critical=False
    )

    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    )

    # return CSR
    return builder.sign( private_key, hashes.SHA256() )
