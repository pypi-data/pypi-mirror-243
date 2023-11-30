import bitmath
from neo.clis.base import Base
from neo.libs import vm as vm_lib
from neo.libs import orchestration as orch
from neo.libs import utils, image
from tabulate import tabulate


class VMCommand(Base):
    """
    usage:
        vm ls
        vm on <VM_ID>
        vm off <VM_ID>  
        vm reboot <VM_ID>
        vm suspend <VM_ID>  
        vm unsuspend <VM_ID>

    Options:
    -h --help                    Print usage
    """

    def execute(self):
        if self.args["ls"]:
            try:
                data_instance = list()
                for instance in vm_lib.get_list():
                    pre_instance = [instance.id, instance.name, instance.key_name]
                    pre_instance.append(image.detail(instance.image["id"]).name)
                    flavors = vm_lib.detail_flavor(instance.flavor["id"])
                    flavors_name = flavors.name
                    flavors_vcpu = flavors.vcpus
                    flavors_ram = bitmath.MiB(flavors.ram).to_GiB().best_prefix()
                    pre_instance.append(flavors_name)
                    pre_instance.append(flavors_ram)
                    pre_instance.append(flavors_vcpu)

                    # Address
                    addr = list()
                    addr_objs = utils.get_index(instance.addresses)
                    if len(addr_objs) > 0:
                        for addr_obj in addr_objs:
                            addr.append("network : {}".format(addr_obj))
                            for addr_ip in instance.addresses[addr_obj]:
                                addr_meta = "{} IP : {}".format(
                                    addr_ip["OS-EXT-IPS:type"], addr_ip["addr"]
                                )
                                addr.append(addr_meta)
                    if len(addr) > 0:
                        pre_instance.append("\n".join(addr))
                    else:
                        pre_instance.append("")

                    pre_instance.append(instance.status)
                    data_instance.append(pre_instance)

                if len(data_instance) == 0:
                    utils.log_err("No Data...")
                    print(self.__doc__)

            except Exception as e:
                utils.log_err(e)
                exit()

            print(
                tabulate(
                    data_instance,
                    headers=[
                        "ID",
                        "Name",
                        "Key Pair",
                        "Image",
                        "Flavor",
                        "RAM (GiB)",
                        "vCPU",
                        "Addresses",
                        "Status",
                    ],
                    tablefmt="grid",
                )
            )
            exit()

        if self.args["on"]:
            instance_id = self.args["<VM_ID>"]
            try:
                do_start = vm_lib.start_instance(instance_id)
                utils.log_info("Instance procceed powered on")
            except Exception as err:
                utils.log_err(err)
            exit()

        if self.args["off"]:
            instance_id = self.args["<VM_ID>"]
            try:
                do_off = vm_lib.stop_instance(instance_id)
                if do_off:
                    utils.log_info("Instance will shutdown!")
            except Exception as err:
                utils.log_err(err)
            exit()

        if self.args["reboot"]:
            instance_id = self.args["<VM_ID>"]
            try:
                do_reboot = vm_lib.reboot_instance(instance_id)
                utils.log_info("Instance rebooting...")
            except Exception as err:
                utils.log_err(err)
            exit()

        if self.args["suspend"]:
            instance_id = self.args["<VM_ID>"]
            try:
                do_suspend = vm_lib.suspend(instance_id)
                utils.log_info("Instance procceed to suspend")
            except Exception as err:
                utils.log_err(err)
            exit()

        if self.args["unsuspend"]:
            instance_id = self.args["<VM_ID>"]
            try:
                do_unsuspend = vm_lib.resume(instance_id)
                utils.log_info("Instance unsuspend...")
            except Exception as err:
                utils.log_err(err)
            exit()
