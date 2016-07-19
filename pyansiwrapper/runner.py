from pyansiwrapper.core.task_executor import TaskExecutor


class Task(object):
    """
    Describes a task.
    """
    def __init__(self, module_name):
        self.module_name = module_name
        self.module_args = None
        self.register_var = None

    @classmethod
    def module(cls, name):
        """
        Creates task with module.
        """
        return cls(name)

    def args(self, module_args):
        """
        Adds module arguments

        Can be a dict as well as the psoitional argument (value)
        """
        self.module_args = module_args
        return self

    def register(self, var):
        """
        Registers variable.
        """
        self.register_var = var
        return self

    def to_task_dict(self):
        """
        Converts task to the dict.
        """
        return dict(action=dict(module=self.module_name,
                                args=self.module_args or ()),
                    register=self.register_var)


class AdHoc(object):
    """
    Run several tasks in a row.
    """

    def __init__(self, inventory_file=None):
        self.inventory_file = inventory_file
        self.verbose = 4
        self.hosts_names = None
        self._tasks = []

    def hosts(self, hosts):
        """
        Specifies the hosts pattern to run tasks on.
        """
        self.hosts_names = hosts
        return self

    def task(self, task):
        """
        Adds new task to the play
        """
        self._tasks.append(task.to_task_dict())
        return self

    def run(self):
        """
        Starts the play.
        """
        executor = TaskExecutor(self.hosts_names,
                                inventory_file=self.inventory_file,
                                verbose=self.verbose)
        executor.add_tasks(self._tasks)
        executor.run()


class Playbook(object):
    """
    The playbook runner.
    """
    pass
