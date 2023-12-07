using Conductor.Client.Worker;
using System;
using Conductor.Client;
using Conductor.Client.Authentication;
using Conductor.Client.Extensions;
using Conductor.Client.Interfaces;
using Conductor.Client.Models;
using Conductor.Definition;
using Conductor.Executor;
using CsWorker;
using Microsoft.Extensions.Logging;


var config1 = new Configuration()
{
    AuthenticationSettings = new OrkesAuthenticationSettings("4af1da52-28d5-489c-b9b1-b7ffc32a0fe8",
        "fLm9JZ1d5pnBxmtOXnaGiea6u84SQ1u8TaNvxjwx2FcHdCDS"),
    //BasePath = "http://localhost:8080/api"
};

var executor = new WorkflowExecutor(config1);
for (var i = 0; i < 100; i++)
{
    Console.WriteLine($"Executing workflow {i}");
    executor.StartWorkflow(new StartWorkflowRequest(
        input: new Dictionary<string, object>() {{"Age", new Random().NextInt64(30)}},
        name: "DoThignWorkflow"));
}

var host1 = WorkflowTaskHost.CreateWorkerHost(
    config1,
    logLevel: LogLevel.Debug,
    workers: new SimpleWorker());
var host2 = WorkflowTaskHost.CreateWorkerHost(
    config1,
    logLevel: LogLevel.Debug,
    workers: new BarBouncer());
await host1.StartAsync();
await host2.StartAsync();
Console.WriteLine("Done");
Console.ReadLine();
Console.WriteLine("Super done");