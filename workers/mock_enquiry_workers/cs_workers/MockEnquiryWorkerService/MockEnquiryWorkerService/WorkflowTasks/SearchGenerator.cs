using Conductor.Client.Extensions;
using Conductor.Client.Interfaces;
using Conductor.Client.Models;
using Conductor.Client.Worker;
using MockEnquiryWorkerService.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Task = Conductor.Client.Models.Task;

namespace MockEnquiryWorkerService.WorkflowTasks;

public class SearchGenerator : BaseWorker
{
    public override string TaskType { get; }
    public override WorkflowTaskExecutorConfiguration WorkerSettings { get; }

    public SearchGenerator(string taskType = "search_generator")
    {
        TaskType = taskType;
        WorkerSettings = new WorkflowTaskExecutorConfiguration() {PollInterval = TimeSpan.FromMilliseconds(1)};
    }
    
    public override TaskResult Execute(Task task)
    {
        var input = task.InputData;
        var enquiryMetadata = input["enquiry_metadata"] as EnquiryMetadata;
        var searchSpecifications = new[]
        {
            new SearchSpecification(DataProviderIdentifier.Google,
                new GoogleSearchRequest(enquiryMetadata.Subject.Item), enquiryMetadata)
        };

        Console.WriteLine("SearchGenerator Happened!");
        return task.Completed(outputData: new Dictionary<string, object>()
            {{"search_specifications", searchSpecifications}});

    }
}