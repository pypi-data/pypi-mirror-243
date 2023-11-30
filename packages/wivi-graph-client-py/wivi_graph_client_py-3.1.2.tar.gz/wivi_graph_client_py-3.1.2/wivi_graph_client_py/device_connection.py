class Device_Connections_Query:
    get_device_connection_query = """
        query GetDeviceConnection($input: DeviceConnectionFilterInput) {
            deviceConnection(input: $input) {
                configuration:{
                    vehicleId
                    fleetId
                    organizationId
                    deviceId
                }
                bytesReceived
                bytesSent
                networkProvider
                network
                networkType
                version
                startTime
                endTime
                time
            }
        }
    """


class Device_Connections_Mutation:

    upsert_device_connection_mutation = '''
        mutation UpsertDeviceConnection($input: CreateDeviceConnectionInput) {
            createDeviceConnection(input: $input) {
                configuration {
                    vehicleId
                    fleetId
                    organizationId
                    deviceId
                }
                bytesReceived
                bytesSent
                networkProvider
                network
                networkType
                version
                startTime
                endTime
                time
            }
        }
    '''

    delete_device_connection_mutation = '''
        mutation DeleteDeviceConnection($input: DeleteDeviceConnectionInput) {
            deleteDeviceConnection(input: $input) {
                DeviceConnection
            }
        }
    '''
