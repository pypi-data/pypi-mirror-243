import sys
import argparse
import time
from pathlib import Path

from . import csrutils
from cryptography.hazmat.primitives import serialization

default_path = Path.home() / "csr"


def gencsr():
    """
    CLI-command `csr` to generate CSR with DNS-names
    """
    parser = argparse.ArgumentParser(description='Generate CSRs', epilog="IP-Addresses are also supported in FQDN/DNS-names by prefixing with 'ip:' (ip:10.1.2.3 in example)")
    parser.add_argument('names', metavar='FQDN', type=str, nargs='+', help='DNS-names for CSR (first will be used for CN)')
    parser.add_argument('--ou', type=str, default="IT", help="Organizational Unit (default: IT)")
    parser.add_argument('--country', type=str, default='NO', help='Two-letter country-code (default: NO)')
    parser.add_argument('--org', type=str, required=True, help='Organization Name')
    parser.add_argument('-w', metavar='PATH', dest='path', type=str, default=default_path, help=f'Output directory (default: {default_path})')
    parser.add_argument('-k', metavar='LEN', dest='key_size', type=int, default=4096, help='Length of RSA private key (default: 4096)')
    args = parser.parse_args()

    # sanity checks
    output_dir = Path(args.path)
    output_dir.mkdir(mode=0o750, exist_ok=True)
    output_dir.chmod(mode=0o755)

    # Sanity check key_size
    key_size = args.key_size

    # check that first name is not an IP
    if csrutils.ip_exp.match(args.names[0]):
        print(f'Error: First names-arg is used as FQDN and cannot be an IP ({args.names[0]})', file=sys.stderr)
        sys.exit(1)

    # validate key_size    
    try: 
        csrutils.validate_key_size(key_size)
    except ValueError:
        print(f'Invalid key size, valid sizes are: {", ".join(map(str, csrutils.valid_rsa_key_sizes))}', file=sys.stderr)
        sys.exit(1)

    key = csrutils.generate_private_key(key_size)

    try:
        csr = csrutils.generate_csr(org=args.org, ou=args.ou, c=args.country,
                            dns_names=args.names, private_key=key)
    except ValueError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


    # name
    base_name = f'{args.names[0]}-{int(time.time())}'

    # write key
    with open(output_dir / f'{base_name}.key', 'wb') as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f'Wrote key: {output_dir / base_name}.key')

    # write csr
    with open(output_dir / f'{base_name}.csr', 'wb') as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))
    print(f'Wrote csr: {output_dir / base_name}.csr')
