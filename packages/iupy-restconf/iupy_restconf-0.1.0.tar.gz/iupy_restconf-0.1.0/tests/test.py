import logging
import iupy_restconf
import requests


if __name__ == "__main__":
    print ("Starting Test Run...")
    logging.basicConfig(level=logging.DEBUG)

    rcs = iupy_restconf.RestConf()

    state = rcs.connect(transport="https", host="testhost", un="testuser", pw="testpass")

    if state is True:
        print("Connection complete.")
    else:
        print("Connection failed: {}".format(state))
        exit(1)

    # Load top-level data
    rcs.get_yang_date()
    rcs.get_operations_resources()
    rcs.get_data_modules()
    rcs.get_netconf_state()

    # Specific displays and checks.
    print("YANG Library Version: {}\n".format(rcs.yang_library['ietf-restconf:yang-library-version']))

    oper_resource = "Cisco-IOS-XE-rpc:crypto"
    url = rcs.check_operations_resources(oper_resource)
    if url is not False:
        print("Oper Resource {} at {}.\n".format(oper_resource, url))
    else:
        print("Oper Resource {} not on this device.\n".format(oper_resource))

    data_resource = "ATM-FORUM-TC-MIB"
    if rcs.check_data_module(data_resource):
        print("Data resource {} found.\n".format(data_resource))
    else:
        print("Data resource {} not found.\n".format(data_resource))

    bgp_rev = rcs.check_data_module("BGP4-MIB")['revision']
    if bgp_rev == "1994-05-05":
        print("BGP Revision OK!\n")
    else:
        print("BGP Revision {}\n".format(bgp_rev))

    print("Operations Module List")
    print("----------------------")
    rcs.show_operations_resources()

    print("\nData Module List")
    print("----------------")
    rcs.show_data_modules()
