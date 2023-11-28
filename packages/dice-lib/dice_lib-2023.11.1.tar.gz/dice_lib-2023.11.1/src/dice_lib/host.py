from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

OUTPUT_PROCESSING_FUNCTIONS = {
    "noop": lambda x: x,
    "to_lower": lambda x: x.lower(),
    "to_upper": lambda x: x.upper(),
    "split_unique_join": lambda x: ",".join(set(x.split(","))),
    "strip_final_newline": lambda x: x.rstrip("\n"),
}


@dataclass
class HostCommand:
    command: str
    parameters: List[str] = field(default_factory=list)
    default_processing_function: Callable[[str], str] = field(
        repr=False, default=OUTPUT_PROCESSING_FUNCTIONS["strip_final_newline"]
    )
    output_processing: Optional[List[Callable[[str], str]]] = field(
        repr=False, default=None
    )

    def __repr__(self) -> str:
        params = " ".join(self.parameters)
        return f"{self.command} {params}"


@dataclass
class PuppetCommand(HostCommand):
    def __init__(
        self,
        command: str,
        parameters: Optional[List[str]] = None,
        output_processing: Optional[List[Callable[[str], str]]] = None,
    ):
        puppet_command = "puppet"
        puppet_parameters = ["agent", command] + (parameters or [])
        super().__init__(
            puppet_command, puppet_parameters, output_processing=output_processing
        )


@dataclass
class FacterCommand(HostCommand):
    def __init__(
        self,
        command: str,
        parameters: Optional[List[str]] = None,
        output_processing: Optional[List[Callable[[str], str]]] = None,
    ):
        facter_command = "facter"
        facter_parameters = [command] + (parameters or [])
        super().__init__(
            facter_command, facter_parameters, output_processing=output_processing
        )


HOST_PROPERTIES: Dict[str, HostCommand] = {
    "hostname": HostCommand(command="hostname", parameters=["-s"]),
    "fqdn": HostCommand(command="hostname", parameters=["-f"]),
    "ip_addresses": HostCommand(
        command="hostname",
        parameters=["-i"],
        output_processing=[
            OUTPUT_PROCESSING_FUNCTIONS["split_unique_join"],
        ],
    ),
    "os_type": HostCommand(command="uname", parameters=["-s"]),
    "Operating System": HostCommand(command="cat", parameters=["/etc/redhat-release"]),
    "domain": HostCommand(command="hostname", parameters=["-d"]),
    "kernel": HostCommand(command="uname", parameters=["-r"]),
    "architecture": HostCommand(command="uname", parameters=["-m"]),
    "cpu_count": HostCommand(command="nproc", parameters=[]),
    "host_names": HostCommand(
        command="hostname",
        parameters=["-A"],
        output_processing=[
            OUTPUT_PROCESSING_FUNCTIONS["split_unique_join"],
        ],
    ),
}

PUPPET_COMMANDS = {
    "puppet_version": PuppetCommand(command="--version"),
    "puppet_managed": PuppetCommand(command="--configprint", parameters=["server"]),
    "puppet_environment": PuppetCommand(
        command="--configprint", parameters=["environment"]
    ),
    "puppet_run_interval": PuppetCommand(
        command="--configprint", parameters=["runinterval"]
    ),
}

FACTER_COMMANDS = {
    "facter_version": FacterCommand(command="--version"),
    "uptime": FacterCommand(command="uptime"),
    "kernel": FacterCommand(command="kernel"),
    "role": FacterCommand(command="node_info.role"),
    "service_name": FacterCommand(command="node_info.service_name"),
    "owner": FacterCommand(command="node_info.owner"),
    "owner_team": FacterCommand(command="node_info.owner_team"),
    "building": FacterCommand(command="node_info.building"),
    "data_centre": FacterCommand(command="node_info.data_centre"),
    "location": FacterCommand(command="node_info.location"),
    "rack": FacterCommand(command="node_info.rack"),
    "position_in_rack": FacterCommand(command="node_info.position_in_rack"),
    "comments": FacterCommand(command="node_info.comments"),
    "linked_service_tsm": FacterCommand(command="node_info.linked_service_tsm"),
}


def execute_remote_commands(
    hostname: str, username: str, commands: Dict[str, HostCommand]
) -> Dict[str, str]:
    """
    Executes a dictionary of commands on a remote host.
    Returns a dictionary of outputs of these commands.
    e.g.
       commands = {
           "hostname": HostCommand(command="hostname", args=["-s"]),
           "fqdn": HostCommand(command="hostname", args=["-f"]),
       }
    will return:
       {  "hostname": "<result of 'hostname -s' command>",
          "fqdn": "<result of 'hostname -f' command>",
       }
    """
    from plumbum.machines.paramiko_machine import ParamikoMachine

    remote = ParamikoMachine(hostname, user=username)
    results = {}
    for name, command in commands.items():
        results[name] = remote[command.command](*command.parameters)
        results[name] = command.default_processing_function(results[name])
        if command.output_processing:
            for func in command.output_processing:
                results[name] = func(results[name])

    return results


def current_fqdn() -> str:
    """Returns fully-qualified domain main (FQDN) of current machine"""
    import socket

    return socket.getfqdn()
