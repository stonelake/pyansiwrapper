from collections import namedtuple

import ansible
from ansible.parsing.dataloader import DataLoader
from ansible.utils.display import Display
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager


class TaskExecutor(object):

    def __init__(self, hosts, inventory_file=None, verbose=4):
        self.verbose = verbose
        self.inventory_file = inventory_file
        self.hosts = hosts
        self.tasks = []

    def add_tasks(self, task_dicts):
        self.tasks.extend(task_dicts)

    def clear_tasks(self):
        self.tasks = []

    def run(self):
        display = Display(verbosity=self.verbose)
        import __main__ as main
        setattr(main, "display", display)

        default_options = {'subset': None, 'ask_pass': False,
                           'listtags': None,
                           'become_user': 'root', 'sudo': False,
                           'private_key_file': None,
                           'syntax': None, 'skip_tags': None, 'diff': False,
                           'sftp_extra_args': '', 'check': False,
                           'force_handlers': False,
                           'remote_user': None, 'become_method': 'sudo',
                           'vault_password_file': None, 'listtasks': None,
                           'output_file': None, 'ask_su_pass': False,
                           'new_vault_password_file': None,
                           'listhosts': None, 'ssh_extra_args': '',
                           'tags': 'all', 'become_ask_pass': False,
                           'start_at_task': None,
                           'flush_cache': None, 'step': None,
                           'module_path': None,
                           'su_user': None, 'ask_sudo_pass': False,
                           'su': False,
                           'scp_extra_args': '', 'connection': 'smart',
                           'ask_vault_pass': False, 'timeout': 30,
                           'become': False,
                           'sudo_user': None, 'ssh_common_args': ''}
        default_options.update(
            verbosity=self.verbose,
            forks=ansible.constants.DEFAULT_FORKS,
            remote_user=ansible.constants.DEFAULT_REMOTE_USER,
            private_key_file=ansible.constants.DEFAULT_PRIVATE_KEY_FILE,
        )

        options = namedtuple('Options', default_options.keys())(
            **default_options)

        # initialize needed objects
        variable_manager = VariableManager()
        loader = DataLoader()
        passwords = dict(vault_pass='secret')

        # create inventory and pass to var manager
        inventory = Inventory(loader=loader,
                              variable_manager=variable_manager,
                              host_list=self.inventory_file)
        variable_manager.set_inventory(inventory)

        # create play with tasks
        play_source = dict(
            name="Ansible AdHoc Play",
            hosts=self.hosts,
            tasks=self.tasks
        )
        play = Play().load(play_source, variable_manager=variable_manager,
                           loader=loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback='default',
            )
            result = tqm.run(play)
            return result
        finally:
            if tqm is not None:
                tqm.cleanup()

