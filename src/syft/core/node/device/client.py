# external class imports
from typing_extensions import final
from typing import Optional
from typing import List

# syft imports
from ...io.location import SpecificLocation
from ....decorators import syft_decorator
from syft.core.common.uid import UID
from ...io.location import Location
from ..common.client import Client
from ...io.route import Route


@final
class DeviceClient(Client):

    device: SpecificLocation  # redefine the type of self.device to not be optional

    @syft_decorator(typechecking=True)
    def __init__(
        self,
        name: str,
        routes: List[Route],
        device: SpecificLocation,
        network: Optional[Location] = None,
        domain: Optional[Location] = None,
        vm: Optional[Location] = None,
    ):
        super().__init__(
            name=name,
            routes=routes,
            network=network,
            domain=domain,
            device=device,
            vm=vm,
        )

    # def create_vm(self, name:str):
    #
    #     # Step 1: create a old_message which will request for a VM to be created.
    #     # we can set route=None because we know the old_message is just going directly
    #     # to the device.
    #     msg = CreateVirtualMachineMessage(vm_name=name, address=self.node_address)
    #
    #     # Step 2: Send the old_message to the device this client points to.
    #     # Receive a reply_msg and save it in a variable.
    #     reply_msg = self.send_msg(msg=msg)
    #
    #     # Step 3: Unpack the vm client from the reply old_message
    #     vm_client = reply_msg.client
    #
    #     # Step 4: Return the client object directly. We assume that the
    #     # client object knows how to send old_message to the VM no matter
    #     # where it exists. Aka, we don't need to save the client in any
    #     # particular kind of context to know how to use it. We should be
    #     # able to "just use it" anywhere and it should "just work"... finding
    #     # the appropriate VM.
    #     return vm_client

    @property
    def id(self) -> UID:
        """This client points to a vm, this returns the id of that vm."""
        return self.device.id

    @property
    def vm(self) -> Optional[Location]:
        """This client points to an node, if that node lives within a vm
        or is a vm itself, this property will return the Location of that vm
        if it is known by the client."""

        return super().vm

    @vm.setter
    def vm(self, new_vm: Location) -> Optional[Location]:
        """This client points to an node, if that node lives within a vm
        or is a vm itself and we learn the Location of that vm, this setter
        allows us to save the Location of that vm for use later. We use a getter
        (@property) and setter (@set) explicitly because we want all clients
        to efficiently save an address object for use when sending messages to their
        target. That address object will include this information if it is available"""

        raise Exception("This client points to a Device, you don't need a VM Location.")

    def __repr__(self) -> str:
        return f"<DeviceClient:{self.device}>"