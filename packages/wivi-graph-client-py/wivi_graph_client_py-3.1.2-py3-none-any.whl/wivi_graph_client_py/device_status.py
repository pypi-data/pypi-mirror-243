class Device_Status_Query:
    get_device_status_query = """
        query GetDeviceStatus($input: DeviceStatusFilterInput) {
            deviceStatus(input: $input) {
                vehicleId
                deviceStatusData {
                    name
                    data {
                        time
                        svalue
                        value
                    }
                }
            }
        }
    """

class Device_Status_Mutation:
    create_device_status_mutation = '''
        mutation CreateDeviceStatus($input: CreateDeviceStatusInput) {
            createDeviceStatus(input: $input) {
                configurationId
            }
        }
    '''

    delete_device_status_mutation = '''
        mutation DeleteDeviceStatus($input: DeleteDeviceStatusInput) {
            deleteDeviceStatus(input: $input) {
                configurations
            }
        }
    '''
