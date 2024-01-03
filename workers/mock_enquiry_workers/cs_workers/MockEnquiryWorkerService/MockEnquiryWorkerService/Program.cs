using Conductor.Client;
using Conductor.Client.Authentication;
using Conductor.Client.Extensions;
using Conductor.Client.Interfaces;
using Conductor.Client.Models;
using Conductor.Executor;
using Microsoft.AspNetCore.Builder;
using MockEnquiryWorkerService;
using MockEnquiryWorkerService.Models;
using MockEnquiryWorkerService.WorkflowTasks;
using Newtonsoft.Json.Serialization;
using Microsoft.Extensions.Logging;

var builder = WebApplication.CreateBuilder(args);
var orkesApiKey = builder.Configuration["OrkesAuth:KeyId"];
var orkesApiSecret = builder.Configuration["OrkesAuth:KeySecret"];
var config1 = new Configuration()
{
    AuthenticationSettings = new OrkesAuthenticationSettings(
        orkesApiKey,
        orkesApiSecret
    ),
    //BasePath = "http://localhost:8080/api"
};

// Start workflow
if (args.Contains("--workflow") || args.Contains("-w"))
{
    var executor = new WorkflowExecutor(config1);
    for (var i = 0; i < 1; i++)
    {
        Console.WriteLine($"Executing workflow {i}");
        executor.StartWorkflow(new StartWorkflowRequest(
            input: new Dictionary<string, object>()
            {
                {"Subject", new EnquiryInputItem("John Smith", EntityType.Person)},
                {"Context", new EnquiryInputItem("Xapien", EntityType.Organisation)}
            },
            name: "MockEnquiry"));
    }
}

// WORKERS!
var workers = new [] {typeof(InitialiseEnquiry), typeof(SearchGenerator)};
var workers2 = new BaseWorker[] { new InitialiseEnquiry(), new SearchGenerator() };

var host = new HostBuilder().ConfigureServices((Action<HostBuilderContext, IServiceCollection>)((ctx, services) =>
{
    services.AddConductorWorker(config1);
    services.AddConductorWorkflowTask(new InitialiseEnquiry());
    services.AddConductorWorkflowTask(new SearchGenerator());
    services.WithHostedService();
})).ConfigureLogging((Action<ILoggingBuilder>)(logging =>
{
    logging.SetMinimumLevel(LogLevel.Debug);
    logging.AddConsole();
})).Build();

await host.StartAsync();

// var host1 = ConductorHelpers.CreateWorkerHost(
//     config1,
//     logLevel: LogLevel.Debug,
//     workers: workers);

// var host3 = WorkflowTaskHost.CreateWorkerHost(
//     config1,
//     logLevel: LogLevel.Debug,
//     workers: workers2);
//
// var host2 = WorkflowTaskHost.CreateWorkerHost(
//     config1,
//     logLevel: LogLevel.Debug,
//     new BarBouncer(), new BarBouncer());
// await host3.StartAsync();
// await host2.StartAsync();
Console.WriteLine("Done starting worker hosts");
Console.ReadLine();
Console.WriteLine("Super done");