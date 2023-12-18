using Conductor.Client;
using Conductor.Client.Extensions;
using Conductor.Client.Interfaces;

namespace MockEnquiryWorkerService;

public static class ConductorHelpers
{
    public static IHost CreateWorkerHost(
        Configuration configuration,
        LogLevel logLevel = LogLevel.Information,
        params Type[] workers)
    {
        return new HostBuilder().ConfigureServices((ctx, services) =>
        {
            services.AddConductorWorker(configuration);
            foreach (var worker in workers)
            {
                services.AddConductorWorkflowTask(worker);
            }
            services.WithHostedService();
        }).ConfigureLogging(logging =>
        {
            logging.SetMinimumLevel(logLevel);
            logging.AddConsole();
        }).Build();
    }

    public static IServiceCollection AddConductorWorkflowTask(
        this IServiceCollection services,
        Type worker
    )
    {
        services.AddTransient(typeof(IWorkflowTask), worker);
        services.AddTransient(worker);
        return services;
    }
}