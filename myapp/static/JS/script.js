function delete_verification_task(taskId) {
    if (confirm('Are you sure you want to eliminate this?')) {
        // Establece el valor del campo oculto con el ID de la tarea seleccionada
        document.getElementById('task_id').value = taskId;
        // Envía el formulario para eliminar la tarea
        document.querySelector('form').submit();
    }
}
function delete_verification_project(projectid) {
    if (confirm('Are you sure you want to eliminate this?')) {
        // Establece el valor del campo oculto con el ID de la tarea seleccionada
        document.getElementById('project_id').value = projectid;
        // Envía el formulario para eliminar la tarea
        document.querySelector('form').submit();
    }
}