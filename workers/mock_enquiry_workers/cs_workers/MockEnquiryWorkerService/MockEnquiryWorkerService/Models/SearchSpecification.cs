namespace MockEnquiryWorkerService.Models;

public record SearchSpecification(
    DataProviderIdentifier DataProvider,
    object SearchRequest,
    // TODO real system would definitely not pass this through here every time. Probably another way for dynamic fork to access this data
    EnquiryMetadata EnquiryMetadata
);

public record GoogleSearchRequest(string Query);