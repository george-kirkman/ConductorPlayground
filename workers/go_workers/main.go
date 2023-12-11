package main

import (
	conductor "github.com/netflix/conductor/client/go"
	"github.com/netflix/conductor/client/go/task/sample"
)

func main() {
apiClient := client.NewAPIClient(
        nil,
        settings.NewHttpSettings(
            "https://play.orkes.io",
        ),
    )
	c := conductor.NewConductorWorker("http://localhost:8080", 1, 10000)

	c.Start("task_1", "", sample.Task_1_Execution_Function, false)
	c.Start("task_2", "mydomain", sample.Task_2_Execution_Function, true)
}
