import SoftLayer.API
import SoftLayer.auth
import requests
import time

def GET_DATACENTER_LOCATION(datacenter_short_name, client):
    object_filter_locations = {
        "name": {
            "operation": datacenter_short_name,
        }
    }
    #this grabs the datacenter location by short name the is provided in the github ticket
    locations = client['SoftLayer_Location_Datacenter'].getDatacenters(filter=object_filter_locations)
    return locations[0]['id']

def GET_BACKEND_ROUTER(datacenter_id, pod_number, client):
    #this grabs the backend router for the location in other name gives you the router of the location pod this must be checked because if it has never been created i dont think you can do so via api
    routers = client['SoftLayer_Location_Datacenter'].getBackendHardwareRouters(id=datacenter_id)
    return routers[pod_number - 1]["id"]

def ORDER_VLAN(dc_location_id, backend_router, name, client, private=True):
    if private == True:
        package_id = 571
        vlan_id = 1072
        vlan_price_id = 27270
        vlan_description = "PRIVATE_NETWORK_VLAN"
    else:
        package_id = 571
        vlan_id = 1071
        vlan_price_id = 29247
        vlan_description = "PUBLIC_NETWORK_VLAN"

    vlan_order = {
        'complexType': 'SoftLayer_Container_Product_Order_Network_Vlan',
        'quantity': 1,
        'location': dc_location_id,
        'packageId': package_id,
        'prices': [
            {
                'id': vlan_price_id,
                'item':{
                    'id': vlan_id,
                    'keyName': vlan_description
                }
            }
        ],
        'name': name,
        'routerId': backend_router
    }

    #///////////////////////
    # this will verify the order
    result = client['SoftLayer_Product_Order'].verifyOrder(vlan_order)
    final = client['SoftLayer_Product_Order'].placeOrder(vlan_order)
    vs_vlan_id_real = final['placeOrder']['items'][0]['id']
    return final

def GET_VLAN_ID(vlan_name, client):
    object_filter = {
        "networkVlans": {
            "name": {
                "operation": vlan_name
            }
        }
    }
    object_mask = "mask[id,vlanNumber,name]"
    get_vlan = client['SoftLayer_Account'].getNetworkVlans(mask=object_mask, filter=object_filter)
    while True:
        try:
            get_vlan = client['SoftLayer_Account'].getNetworkVlans(mask=object_mask, filter=object_filter)
            get_vlan[0]['id']
        except IndexError:
            print("sleeping")
            time.sleep(5)
            continue
        else:
            break
    return get_vlan

def ORDER_SUBNET_CREATOR(dc_location_id, vlan_id, name, client):
    vs_response_price_id = 32627
    vs_response_id = 52
    vs_ram_price_id = 22694
    vs_ram_id = 863
    vs_computing_price_id = 25752
    vs_computing_id = 858
    vs_disk_price_id = 32578
    vs_disk_id = 1178
    vs_monitoring_price_id = 27023
    vs_monitoring_id = 49
    vs_notification_price_id = 32500
    vs_notification_id = 51
    vs_remote_price_id = 23070
    vs_remote_id = 503
    vs_vpn_price_id = 16594
    vs_vpn_id = 309
    vs_public_bandwidth_price_id = 35963
    vs_public_bandwidth_id = 4481
    vs_primary_address_price_id = 34807
    vs_primary_address_id = 15
    vs_network_uplink_id = 497
    vs_network_uplink_price_id = 23787
    vs_centos_id = 28027
    vs_centos_price_id = 307615
    vs_package_id = 46
    vlan_id_private = 1079200889
    vs_order = {
        'complexType': 'SoftLayer_Container_Product_Order_Virtual_Guest',
        'quantity': 1,
        'location': dc_location_id,
        'packageId': vs_package_id,
        'prices': [
            {
                #os centos 9.x define
                'id':vs_centos_price_id,
                'item':{
                    'id': vs_centos_id,
                    'keyName': 'OS_CENTOS_STREAM_9_X_MINIMAL_64_BIT',
                }
            },
            {
                #private network uplink
                'id':vs_network_uplink_price_id,
                'item':{
                    'id': vs_network_uplink_id,
                    'keyName': '100_MBPS_PRIVATE_NETWORK_UPLINK',
                }

            },
            {
                #primary ip address
                'id':vs_primary_address_price_id,
                'item':{
                    'id': vs_primary_address_id,
                    'keyName': '1_IP_ADDRESS',
                }
            },
            {
                #public bandwidth
                'id':vs_public_bandwidth_price_id,
                'item':{
                    'id': vs_public_bandwidth_id,
                    'keyName': 'BANDWIDTH_0_GB',
                }
            },
            {
                #vpn managment
                'id':vs_vpn_price_id,
                'item':{
                    'id': vs_vpn_id,
                    'keyName': 'UNLIMITED_SSL_VPN_USERS_1_PPTP_VPN_USER_PER_ACCOUNT',
                }
            },
            {
                #remote management
                'id':vs_remote_price_id,
                'item':{
                    'id': vs_remote_id,
                    'keyName': 'REBOOT_REMOTE_CONSOLE',
                }
            },
            {
                #notification
                'id':vs_notification_price_id,
                'item':{
                    'id': vs_notification_id,
                    'keyName': 'NOTIFICATION_EMAIL_AND_TICKET',
                }
            },
            {
                #monitoring
                'id':vs_monitoring_price_id,
                'item':{
                    'id': vs_monitoring_id,
                    'keyName': 'MONITORING_HOST_PING',
                }
            },
            {
                #first disk
                'id':vs_disk_price_id,
                'item':{
                    'id': vs_disk_id,
                    'keyName': 'GUEST_DISK_25_GB_SAN',
                }
            },
            {
                #computing instance
                'id':vs_computing_price_id,
                'item':{
                    'id': vs_computing_id,
                    'keyName': 'GUEST_CORES_2',
                }
            },
            {
                #ram
                'id':vs_ram_price_id,
                'item':{
                    'id': vs_ram_id,
                    'keyName': 'RAM_4_GB',
                }
            },
            {
                #response
                'id':vs_response_price_id,
                'item':{
                    'id': vs_response_id,
                    'keyName': 'AUTOMATED_NOTIFICATION',
                }
            },
        ],
        'hardware': [
            {
                'hostname': f'{name}-subnetcreator',
                'domain': 'bpmoncloud.local',
                'primaryBackendNetworkComponent': {
                    'networkVlanId': vlan_id
                }
            }
        ],
        'operatingSystemReferenceCode': 'CENTOS_STREAM_9_64'
    }

    #///////////////////////////////
    #this will verify and buy the virutal server
    results = client['SoftLayer_Product_Order'].verifyOrder(vs_order)
    return client['SoftLayer_Product_Order'].placeOrder(vs_order)

def GET_GW_ID(gw_device, client):
    object_filter_gateway = {
        "networkGateways": {
            "name": {
                "operation": gw_device
            }
        }
    }
    gatewayID = client['SoftLayer_Account'].getNetworkGateways(filter=object_filter_gateway)
    return gatewayID

def ASSOCIATE_AND_ROUTE_THROUGH_VLAN(gateway_id, vlan_id, client):
    object = {
        "bypassFlag": False,
        "networkGatewayId": gateway_id,
        "networkVlanId": vlan_id,
    }
    template = []
    template.append(object)
    result_vlan_route = client['SoftLayer_Network_Gateway_Vlan'].createObjects(template)
    return result_vlan_route

def GET_SUBNETS(vlan_id, client):
    subnet_object_mask = "mask[subnets]"
    return client['SoftLayer_Network_Vlan'].getObject(id=vlan_id, mask=subnet_object_mask)