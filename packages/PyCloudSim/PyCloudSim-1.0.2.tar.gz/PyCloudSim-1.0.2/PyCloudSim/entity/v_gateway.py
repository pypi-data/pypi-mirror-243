from __future__ import annotations
from math import inf
from operator import indexOf
from typing import TYPE_CHECKING, List

from Akatosh import Entity, EntityList, Resource
from Akatosh.entity import Entity

from PyCloudSim import simulation, logger

from .v_nic import vNIC
from .constants import Constants

if TYPE_CHECKING:
    from .v_packet import vPacket
    from .v_user import vUser


class vGateway(Entity):
    def __init__(
        self,
        label: str | None = None,
    ) -> None:
        super().__init__(label=label, create_at=0)

        self._users: List[vUser] = EntityList()
        self._NIC = vNIC(host=self, label=f"{self}-NIC")
        self._ram = Resource(capacity=inf, label=f"{self}-RAM")
        self._cpu = None

    def on_creation(self):
        simulation.topology.add_node(self)
        self.NIC.create(simulation.now)

    def on_termination(self):
        return super().on_termination()

    def on_destruction(self):
        return super().on_destruction()

    def receive_packet(self, packet: vPacket) -> None:
        if packet.decoded:
            packet.state.remove(Constants.DECODED)
        if packet.in_transmission:
            packet.state.remove(Constants.INTRANSMISSION)
        try:
            packet.get(self.ram, packet.size)
        except:
            packet.drop()
            return
        self.packet_queue.append(packet)
        packet._current_hop = self
        if packet.current_hop is not packet.dst_host:
            packet._next_hop = packet.path[indexOf(packet.path, self) + 1]
        logger.info(f"{simulation.now}:\t{self} receives {packet}.")

    @property
    def users(self) -> List[vUser]:
        return self._users

    @property
    def NIC(self) -> vNIC:
        return self._NIC

    @property
    def ram(self) -> Resource:
        return self._ram

    @property
    def cpu(self):
        return self._cpu

    @property
    def packet_queue(self):
        """Return the packet queue of the hardware entity"""
        return self.NIC.packet_queue
