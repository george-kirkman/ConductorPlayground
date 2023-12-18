namespace MockEnquiryWorkerService.Models;

public record EnquiryMetadata(Guid EnquiryId, EnquiryInputItem Subject, EnquiryInputItem[] Context);

public record EnquiryInputItem(string Item, EntityType Type);

public enum EntityType
{
    Person,
    Organisation
}