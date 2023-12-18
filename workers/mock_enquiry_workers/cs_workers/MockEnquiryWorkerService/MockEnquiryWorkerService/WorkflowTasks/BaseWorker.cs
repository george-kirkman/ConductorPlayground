using Conductor.Client.Interfaces;
using Conductor.Client.Models;
using Conductor.Client.Worker;
using Task = Conductor.Client.Models.Task;

namespace MockEnquiryWorkerService.WorkflowTasks;

public abstract class BaseWorker : IWorkflowTask
{
    public abstract TaskResult Execute(Task task);

    public abstract string TaskType { get; }
    public abstract WorkflowTaskExecutorConfiguration WorkerSettings { get; }
}