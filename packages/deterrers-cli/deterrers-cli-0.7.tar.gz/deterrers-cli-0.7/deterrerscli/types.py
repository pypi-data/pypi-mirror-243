import click
import ipaddress
import socket


class IPv4Type(click.ParamType):
    '''Click parameter type for IPv4 address.
    Also accepts domain names if they can be resolved to an IPv4 address.
    '''
    name = 'IPv4 address'

    def convert(self, value, param, ctx):
        try:
            ipaddress.IPv4Address(value)
            return value
        except ipaddress.AddressValueError:
            pass

        try:
            return socket.gethostbyname(value)
        except socket.gaierror:
            pass

        self.fail(f'{value!r} cannot be resolved to IPv4 address', param, ctx)


IPV4_TYPE = IPv4Type()

PROFILE_TYPE = click.Choice(
        ('', 'HTTP', 'SSH', 'HTTP+SSH', 'Multipurpose'),
        case_sensitive=False)

HOST_FIREWALL_TYPE = click.Choice(
        ('', 'UFW', 'FirewallD', 'nftables'),
        case_sensitive=False)

OUTPUT_TYPE = click.Choice(
        ('json', 'yaml'),
        case_sensitive=False)
