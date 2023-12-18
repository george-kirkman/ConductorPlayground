using Conductor.Client.Extensions;
using Conductor.Client.Interfaces;
using Conductor.Client.Models;
using Conductor.Client.Worker;
using Task = Conductor.Client.Models.Task;

namespace MockEnquiryWorkerService.WorkflowTasks;

public class InitialiseEnquiry : BaseWorker
{
    public override string TaskType { get; }
    public override WorkflowTaskExecutorConfiguration WorkerSettings { get; }

    public InitialiseEnquiry(string taskType = "initialise_enquiry")
    {
        TaskType = taskType;
        WorkerSettings = new WorkflowTaskExecutorConfiguration() {PollInterval = TimeSpan.FromMilliseconds(1)};
    }
    
    public override TaskResult Execute(Task task)
    {
        var input = task.InputData;
        // Real world will do checks on inputs and spin up resources etc.
        input.Add("enquiry_id", Guid.NewGuid()); //.ToString()?

        Console.WriteLine("InitialiseEnquiry Happened!");
        return task.Completed(outputData: input);
    }
}