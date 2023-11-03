function delete_verification(taskId) {
    if (confirm('Are you sure you want to eliminate this task?')) {
        // Establece el valor del campo oculto con el ID de la tarea seleccionada
        document.getElementById('task_id').value = taskId;
        // Envía el formulario para eliminar la tarea
        document.querySelector('form').submit();
    }
}