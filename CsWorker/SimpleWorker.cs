using Conductor.Client.Extensions;
using Conductor.Client.Interfaces;
using Conductor.Client.Models;
using Conductor.Client.Worker;
using Newtonsoft.Json.Linq;
using Task = Conductor.Client.Models.Task;

namespace CsWorker;

public class SimpleWorker : IWorkflowTask
{
    public string TaskType { get; }
    public WorkflowTaskExecutorConfiguration WorkerSettings { get; }

    public SimpleWorker(string taskType = "DoThign")
    {
        TaskType = taskType;
        WorkerSettings = new WorkflowTaskExecutorConfiguration() {PollInterval = TimeSpan.FromSeconds(3)};
    }
    
    public TaskResult Execute(Task task)
    {
        var input = task.InputData;
        var age = (long) input["Age"];

        var isOver18 = age > 18;

        Console.WriteLine("DoThign Happened!");
        return task.Completed(outputData: new Dictionary<string, object>()
            {{"blah", "omg it works"}, {"IsOver18", isOver18}});

    }
}

public class BarBouncer : IWorkflowTask
{
    public string TaskType { get; }
    public WorkflowTaskExecutorConfiguration WorkerSettings { get; }

    public BarBouncer(string taskType = "WelcomeToBar")
    {
        TaskType = taskType;
        WorkerSettings = new WorkflowTaskExecutorConfiguration() {PollInterval = TimeSpan.FromMilliseconds(1)};
    }

    public TaskResult Execute(Task task)
    {
        var input = task.InputData;
        var doThingResult = JObject.FromObject(input["DoThignResult"]);
        var isOver18 = (bool) doThingResult["IsOver18"];

        var message = isOver18
            ? "Hello there! Take a nice cool refreshing beverage on the house!"
            : "Please leave. I don't like you >:( You are TOO YOUNG!";
        Console.WriteLine("BarBouncer happened!");
        return task.Completed(outputData: new Dictionary<string, object>() {{"BarGreetings", message}});
    }
}