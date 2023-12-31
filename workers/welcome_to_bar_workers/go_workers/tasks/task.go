package task

import (
	"log"

	"github.com/netflix/conductor/client/go/task"
)

// Implementation for "task_1"
func Task_1_Execution_Function(t *task.Task) (taskResult *task.TaskResult, err error) {
	log.Println("Executing Task_1_Execution_Function for", t.TaskType)

	//Do some logic
	taskResult = task.NewTaskResult(t)

	output := map[string]interface{}{"task": "task_1", "key2": "value2", "key3": 3, "key4": false}
	taskResult.OutputData = output
	taskResult.Status = "COMPLETED"
	err = nil

	return taskResult, err
}
