class Device_Version_Query:
    get_device_version_query = """
        query GetDeviceInfo($input: DeviceInfoFilterInput) {
            deviceInfo(input: $input) {
                vehicleId
                deviceInfoData {
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
class Device_Version_Mutation:
    upsert_device_version_mutation = '''
        mutation UpsertDeviceVersion($input: UpsertDeviceVersionInput) {
            upsertDeviceVersion(input: $input) {
                configurationId
            }
        }
    '''

    delete_device_version_mutation = '''
        mutation DeleteDeviceVersion($input: DeleteDeviceVersionInput) {
            deleteDeviceVersion(input: $input) {
                configurations
            }
        }
    '''