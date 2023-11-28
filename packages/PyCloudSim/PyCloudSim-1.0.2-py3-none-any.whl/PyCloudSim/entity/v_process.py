from __future__ import annotations
from math import inf

from typing import TYPE_CHECKING, Callable, List

from Akatosh import Entity, EntityList

from PyCloudSim import logger, simulation

from .constants import Constants
from .v_instruction import vInstruction
from .v_sofware_entity import vSoftwareEntity

if TYPE_CHECKING:
    from .v_container import vContainer
    from .v_hardware_entity import vHardwareEntity
    from .v_packet import vPacket


class vProcess(vSoftwareEntity):
    """Simulated process."""

    def __init__(
        self,
        length: int | Callable[..., int],
        priority: int | Callable[..., int] = 0,
        label: str | None = None,
        create_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        terminate_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        precursor: Entity | List[Entity] | None = None,
    ) -> None:
        super().__init__(label, create_at, terminate_at, precursor)

        if callable(length):
            self._length = round(length())
        else:
            self._length = length
        if callable(priority):
            self._priority = round(priority())
        else:
            self._priority = priority

        self._instructions: List[vInstruction] = list()
        self._unscheduled_instructions: List[vInstruction] = EntityList(
            label=f"{self} Unscheduled Instructions"
        )

    def on_initiate(self):
        # initial instructions
        super().on_initiate()
        for i in range(self.length):
            vInstruction(
                process=self,
                create_at=simulation.now,
            )

        @self.continuous_event(
            at=simulation.now,
            interval=simulation.min_time_unit,
            duration=inf,
            label=f"{self.label} Monitor",
        )
        def monitoring():
            if not self.deamon:
                if all([i.terminated for i in self.instructions]):
                    self.success(simulation.now)
                    return

    def on_creation(self):
        super().on_creation()
        logger.info(f"{simulation.now}:\t{self} is created.")
        self.initiate(at=simulation.now)

    def on_termination(self):
        super().on_termination()
        for instruction in self.instructions:
            instruction.terminate(at=simulation.now)
        logger.info(f"{simulation.now}:\t{self} is terminated.")

    def on_destruction(self):
        super().on_destruction()
        for instruction in self.instructions:
            instruction.terminate(at=simulation.now)

    def on_success(self) -> None:
        super().on_success()
        logger.info(f"{simulation.now}:\t{self} is successfully executed.")

    def on_fail(self) -> None:
        super().on_fail()
        logger.info(f"{simulation.now}:\t{self} is failed.")

    @property
    def length(self) -> int:
        """The length of the process"""
        return self._length

    @property
    def priority(self) -> int:
        """The priority of the process"""
        return self._priority

    @property
    def instructions(self):
        """The instructions of the process"""
        return self._instructions

    @property
    def unscheduled_instructions(self):
        """The instructions of the process that has not been scheduled"""
        return self._unscheduled_instructions

    @property
    def host(self):
        """The host that executes this process"""
        return None

    @property
    def container(self):
        """The container that executes this process"""
        return None

    @property
    def deamon(self):
        """The deamon that executes this process"""
        return False


class vContainerProcess(vProcess):
    def __init__(
        self,
        container: vContainer,
        length: int | Callable[..., int],
        priority: int | Callable[..., int] = 0,
        label: str | None = None,
        create_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        terminate_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        precursor: Entity | List[Entity] | None = None,
    ) -> None:
        super().__init__(length, priority, label, create_at, terminate_at, precursor)
        self._container = container

    def on_initiate(self):
        super().on_initiate()
        if self.container is None:
            raise ValueError(f"{self} is not assigned to a container.")

        self.container.process_queue.append(self)
        self.container.host.cpu.process_queue.append(self)

    @property
    def container(self):
        """The container that executes this process"""
        return self._container

    @property
    def host(self):
        """The host that executes this process"""
        return self.container.host


class vDeamon(vProcess):
    def __init__(
        self,
        container: vContainer,
        length: int | Callable[..., int],
        priority: int | Callable[..., int] = 0,
        label: str | None = None,
        create_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        terminate_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        precursor: Entity | List[Entity] | None = None,
    ) -> None:
        super().__init__(length, priority, label, create_at, terminate_at, precursor)
        self._container = container

    def on_initiate(self):
        super().on_initiate()
        if self.container is None:
            raise ValueError(f"{self} is not assigned to a container.")

        self.container.process_queue.append(self)
        self.container.host.cpu.process_queue.append(self)

    def on_fail(self) -> None:
        super().on_fail()
        self.container.fail(simulation.now)

    @property
    def container(self):
        """The container that executes this process"""
        return self._container

    @property
    def host(self):
        """The host that executes this process"""
        return self.container.host

    @property
    def deamon(self):
        return True


class vDecoder(vProcess):
    def __init__(
        self,
        packet: vPacket,
        host: vHardwareEntity,
        length: int | Callable[..., int],
        priority: int | Callable[..., int] = 0,
        label: str | None = None,
        create_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        terminate_at: int
        | float
        | Callable[..., int]
        | Callable[..., float]
        | None = None,
        precursor: Entity | List[Entity] | None = None,
    ) -> None:
        super().__init__(length, priority, label, create_at, terminate_at, precursor)
        self._packet = packet
        self._host = host

    def on_initiate(self):
        super().on_initiate()
        if self.host is None:
            raise ValueError(f"{self} is not assigned to a host.")
        self.host.process_queue.append(self)

    def on_success(self):
        super().on_success()
        self.packet.state.append(Constants.DECODED)
        logger.info(f"{simulation.now}:\t{self.packet} is decoded.")
        if self.packet.current_hop is self.packet.dst_host:
            self.packet.success(simulation.now)

    def on_fail(self) -> None:
        super().on_fail()

    @property
    def packet(self):
        """The packet that is decoded"""
        return self._packet

    @property
    def host(self):
        """The host that decodes the packet"""
        return self._host
