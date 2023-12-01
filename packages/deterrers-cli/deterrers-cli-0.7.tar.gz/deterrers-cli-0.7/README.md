# Command line client for DETERRERS

A command line client making it easy to interact with the DETERRERS perimeter
firewall portal to registr and configuration IP addresses and firewall
profiles.

**Warning:** The API of DETERRERS used by this tool is still experimental and somewhat fragile.
Most notably, this often leads to unexpected errors returned by the API.


## Installation

Use pip to install the latest version:

```
pip install deterrers-cli
```

## Configuration

To configure the client, create a file `~/.deterrers.yml` with the following content:

```yaml
url: https://deterrers.example.com
token: <api-token>

# If you want to automatically register newly added hosts
# Default: false
auto-register: false

# If you want to skip the initial security scan by default.
# Default: false
auto-skip-scan: false
```

## Usane

Use the context based help to get information about available commands:

```
❯ deterrers-cli --help
Usage: python -m deterrerscli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  action  Activate firewall profile or block IP address in perimeter...
  add     Add IP address to DETERRERS.
  delete  Delete IP address from DETERRERS.
  get     Get information about an IP address in DETERRERS.
  hosts   List all IPs added to DETERRERS.
  update  Update IP address in DETERRERS.
```

Help about adding new IP addresses:

```
❯ deterrers-cli add --help
Usage: python -m deterrerscli add [OPTIONS] IPV4

  Add IP address to DETERRERS.

Options:
  -a, --admin TEXT  [required]
  -p, --profile [|HTTP|SSH|HTTP+SSH|Multipurpose]
  -f, --firewall [|UFW|FirewallD|nftables]
  --help            Show this message and exit.
```

## Example

```sh
# Delete IP 192.0.0.1 from DETERRERS
❯ deterrers-cli delete 192.0.0.1

# Add IP 192.0.0.1 with group `virtUOS` as admins and firewall profile `Multipurpose`
❯ deterrers-cli add --admin virtUOS --profile multipurpose 192.0.0.1

# Set firewall profile `SSH`
❯ deterrers-cli update --profile ssh 192.0.0.1

# Activate firewall profile
❯ deterrers-cli action register 192.0.0.1
```


## Shell Completion

The `deterrers-cli` command line tool supports shell completion for several major shells:

For **Bash**, add to `~/.bashrc`:

```
eval "$(_DETERRERS_CLI_COMPLETE=bash_source deterrers-cli)"
```

For **ZSH**, add to `~/.zshrc`:

```
eval "$(_DETERRERS_CLI_COMPLETE=zsh_source deterrers-cli)"
```

For **fish**, add to `~/.config/fish/completions/deterrers-cli.fish`:

```
_DETERRERS_CLI_COMPLETE=fish_source deterrers-cli | source
```
