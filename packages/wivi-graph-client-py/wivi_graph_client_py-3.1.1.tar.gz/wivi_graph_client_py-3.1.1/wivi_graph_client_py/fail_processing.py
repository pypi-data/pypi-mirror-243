class FailProcessingQuery:
    get_failed_processing_query = """
        query GetFailedProcessing($input: FailedProcessingFilterInput) {
            failedProcessing(input: $input) {
                configuration {
                    vehicleId
                    fleetId
                    organizationId
                    vehicleId
                }
                uploadId
                dbExists
                xmlExists
                pipelineStatus
            }
        }
    """

class FailProcessingMutation:
    upsert_failed_processing_mutation = '''
        mutation UpsertFailedProcessing($input: UpsertFailedProcessingInput) {
            upsertFailedProcessing(input: $input) {
                configuration {
                    vehicleId
                    fleetId
                    organizationId
                    vehicleId
                }
                uploadId
                dbExists
                xmlExists
                pipelineStatus
            }
        }
    '''

    delete_failed_processing_mutation = '''
        mutation DeleteFailedProcessing($input: DeleteFailedProcessingInput) {
            deleteFailedProcessing(input: $input) {
                configurations
            }
        }
    '''