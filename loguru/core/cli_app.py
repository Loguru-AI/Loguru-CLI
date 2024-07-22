import os.path
import random
import sys
import traceback

from langchain_core.messages import AIMessage
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from prettytable import PrettyTable
from prompt_toolkit import PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

from loguru import LOGURU_DATA_DIR
from loguru.core.fs_log_rag import LoguruRAG
from loguru.core.models.config import Config

bindings = KeyBindings()


def _help_for_app_exit():
    print("Type /bye to exit or /? for help.")


@bindings.add('c-c')
def confirm_quit_cc(event):
    run_in_terminal(_help_for_app_exit)


@bindings.add('c-d')
def confirm_quit_cd(event):
    run_in_terminal(_help_for_app_exit)


class CLIApp:
    def __init__(self, config: Config, with_tools=False, tool_registry: [] = None):
        self._config = config
        self._with_tools = with_tools
        self._tool_registry = tool_registry
        if with_tools:
            # print("Using tools...")
            pass
        else:
            # print("Using raw mode...")
            pass

    # noinspection PyMethodMayBeStatic
    def _call_tools(self, query: str, model: str, base_url: str, stream: bool = False):
        """
        Make sure to use model 'mistral' for this capability

        :param query:
        :param model:
        :param base_url:
        :param stream:
        :return:
        """
        llm = OllamaFunctions(model=model, base_url=base_url, format="json", temperature=0)
        llm_with_tools = llm.bind_tools(self._tool_registry)
        try:
            # noinspection PyTypeChecker
            response: AIMessage = llm_with_tools.invoke(query)
            if len(response.tool_calls) > 0:
                for tool_call in response.tool_calls:
                    function_name = tool_call['name']
                    function_args = tool_call['args']

                    kwargs_str = ", ".join(f"{key}={repr(value)}" for key, value in function_args.items())
                    eval_statement = f"{function_name}({kwargs_str}).run(config={self._config.dict()}, user_query='{query}')"
                    # print(eval_statement)
                    # print("Calling function: " + eval_statement)
                    # TODO: replace string imports with Pythonic form
                    exec(
                        f'from loguru.core.tool_impls import *;from loguru.core.models.config import *;{eval_statement}')
            else:
                print("Could not process the query.")
                # self._ask_llm_raw(query, model, base_url, stream=True)
        except Exception as e:
            print("Oops, seems like the AI cannot process that!")
            print(e)
            # traceback.print_exc(file=sys.stdout)

    # noinspection PyMethodMayBeStatic

    def _llm_interact(self, input_text: str, with_tools: bool = False, stream: bool = False):
        try:
            if with_tools:
                self._call_tools(
                    query=input_text,
                    model=self._config.ollama.llm_name,
                    base_url=str(random.choice(self._config.ollama.hosts)),
                    stream=False
                )
            else:
                self._ask_llm_raw(
                    query=input_text,
                    stream=False
                )
        except Exception as e:
            print("Oops, we hit a snag!")
            # TODO: Write to log file and prettify the error that user can see
            print(f"Error: {e}")
            traceback.print_exc(file=sys.stdout)

    def _ask_llm_raw(self, query: str, stream: bool = True):
        lg = LoguruRAG(config=self._config)
        lg.scan()
        resp = lg.ask(question=query, stream=stream)

    def scan_and_rebuild_cache(self):
        LoguruRAG(config=self._config).scan(clean_and_rebuild=True)

    def start(self):
        from prompt_toolkit.styles import Style
        from prompt_toolkit.shortcuts import CompleteStyle
        from prompt_toolkit.formatted_text import HTML

        _prompt_style = Style.from_dict({
            'placeholder': '#FF0000',  # Light gray color for the placeholder
        })

        def clear_last():
            # history_file = os.path.join(LOGURU_DATA_DIR, 'history.txt')
            # if os.path.exists(history_file):
            #     with open(history_file, 'r') as history_file_r:
            #         lines = history_file_r.readlines()
            #         lines = lines[:-3]
            #     with open(str(history_file), 'w') as history_file_w:
            #         history_file_w.writelines(lines)
            pass

        history = FileHistory(filename=os.path.join(LOGURU_DATA_DIR, 'history.txt'))

        def _get_user_input():
            prompt_text = '>>> '
            prompt_placeholder = 'Enter your query here (/? for help)'
            session = PromptSession(history=history, enable_history_search=True)

            return session.prompt(
                prompt_text,
                # placeholder='Enter your query here (/? for help)',
                placeholder=HTML(f'<ansigray>{prompt_placeholder}</ansigray>'),
                default='',
                complete_style=CompleteStyle.READLINE_LIKE,
                style=_prompt_style,
                key_bindings=bindings
            )

        def _show_help():
            _cmd_help_dict = {
                '/?': 'Show this help',
                '/history': 'Show history',
                '/bye': 'Exit'
            }
            cols = ["Command", "Description"]
            t = PrettyTable(cols)
            t.align[cols[0]] = "l"
            t.align[cols[1]] = "l"
            for k in _cmd_help_dict:
                t.add_row([k, _cmd_help_dict[k]])
            print(t)

        while True:
            user_input = _get_user_input()
            if user_input == '/bye':
                clear_last()
                break
            elif user_input == '/?':
                clear_last()
                _show_help()
            elif user_input == '/history':
                clear_last()
                for c in history.get_strings():
                    print(c)
            elif user_input.strip() == '':
                continue
            else:
                self._llm_interact(
                    input_text=user_input,
                    with_tools=self._with_tools  # Change to False for raw LLM response
                )
