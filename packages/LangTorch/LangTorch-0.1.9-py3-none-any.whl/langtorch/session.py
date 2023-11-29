import asyncio
import contextvars
import datetime
import hashlib
import logging
import os
from collections import OrderedDict

import torch
import yaml
from omegaconf import OmegaConf
from omegaconf.errors import UnsupportedValueType

from .conf import cfg_yaml_aliases


class SingletonMeta(type):
    _instance = contextvars.ContextVar('ctx',
                                       default={})  # Can i add that what contextvar is set depends on the object class so that i can use the same metaclass for various object?

    def __call__(cls, *args, **kwargs):
        instances = cls._instance.get()
        if cls not in instances:
            instance = super().__call__(*args, **kwargs)
            instances[cls] = instance
            cls._instance.set(instances)
        else:
            if args or kwargs:
                instances[cls].load(*args, **kwargs)
        return instances[cls]


class Session(metaclass=SingletonMeta):
    """A context manager for saving and loading session data: tensors, api calls, configuration and caching"""
    current_session = contextvars.ContextVar('ctx', default={})
    default_session = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf/defaults.yaml")
    session_file_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf/new_session_template.yaml")

    def __init__(self, session_file=None, new_session_file=False):
        self._async_lock = asyncio.Lock()
        self._temp = dict()
        self._open = True
        self._override = new_session_file
        self.load(session_file, new_session_file)

        if not hasattr(self, "_thread_lock_acquired"):
            self._thread_lock_acquired = False

        if not hasattr(self, "tensor_savepath") or getattr(self, "tensor_savepath", None) is None:
            if self._path is None:
                self.tensor_savepath = ""
            else:
                self.tensor_savepath = os.path.join(os.path.dirname(os.path.abspath(self._path)), "saved_tensors.pt")
        assert self.tensor_savepath is not None

    @classmethod
    def load(self, path="$self._path", new_session_file=False):
        """Called to set or change the path and load or reload the config"""
        _config = OmegaConf.load(self.default_session)
        if path == "$self._path":
            path = getattr(self, "_path", None)

        if getattr(self, "_path", torch.nan) == path:
            if self._config:
                _config = OmegaConf.merge(_config, self._config)
        else:
            self._path = path

        if self._path:
            if os.path.exists(self._path) and not new_session_file:  # apply overrides to _config
                try:
                    _config = OmegaConf.merge(_config, OmegaConf.load(self._path))
                except Exception as E:
                    print(f"Error loading session from {self._path}: {E}")
            else:  # create a new session file
                with open(path, "w") as f:
                    with open(self.session_file_template, "r") as f2:
                        f.write(f2.read())
                        logging.warning(
                            f"File not found at {path} when loading new session file. {'Session will not be saved' if not new_session_file else 'Overriding existing session file'}")
        self._config = _config
        return self

    def reload(self):
        """Called to ensure config is up-to-date"""
        return self.load()

    # Synchronous context manager methods
    def __enter__(self):
        self._config = OmegaConf.load(self._path)
        self._open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._open:
            if self._path: OmegaConf.save(self._config, self._path)
        else:
            print("Warning: exiting a Session that was closed, no save performed")

    # Asynchronous context manager methods
    async def __aenter__(self):
        self._config = OmegaConf.load(self._path)
        await self._async_lock.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._path: OmegaConf.save(self._config, self._path)
        self._async_lock.release()

    def open(self):
        self._open = True
        if not self._thread_lock_acquired:
            self._thread_lock.acquire()
            self._thread_lock_acquired = True
        self._config = OmegaConf.load(self._path)
        return self

    def close(self):
        if self._thread_lock_acquired:
            if self._path: OmegaConf.save(self._config, self._path)
            self._thread_lock.release()
            self._thread_lock_acquired = False
        self._open = False
        Session.current_session.set({})

    def add_requests(self, provider, type, job_id, requests):
        _api = dict(self.api)
        if not provider in _api:
            _api[provider] = dict()
        if not type in _api[provider]:
            _api[provider][type] = dict()
        if not job_id in _api[provider][type]:
            _api[provider][type][job_id] = {"requests": requests, "responses": []}
        else:
            _api[provider][type][job_id][requests] += requests

        self.api = _api
        assert self._config.api[provider][type][job_id]["requests"]

    def add_responses(self, provider, type, job_id, responses, override=False):
        """Append an api response payload to response list."""
        self.reload()
        _api = dict(self.api)
        # if self.tensor_savepath=="":
        #     if not job_id in self._temp:
        #         _api[job_id] = {"requests": [], "responses": []}
        #         logging.info("Did not find saved api requests upon saving responses, creating new entry")
        # if override:
        #     _api[job_id]["responses"] = [m[1]["data"][0]["embedding"] for m in responses[0]]
        # else:
        #     _api[job_id]["responses"].append([m[1]["data"][0]["embedding"] for m in responses[0]])

        if override:
            _api[provider][type][job_id]["responses"] = responses
        else:
            _api[provider][type][job_id]["responses"].append(responses)

        self.api = _api

    def get_responses(self, provider, type, job_id=-1):
        self.reload()
        return [job["responses"] if job else None for job in self.get_job(job_id, type, provider)[-1]]

    def get_job(self, job_id=-1, type=None, provider=None):
        self.reload()
        _api = self.api  # if (self.tensor_savepath is not None) else self._temp
        if isinstance(provider, int):
            provider = list(_api.keys())[provider]
        if isinstance(type, int) and provider is not None:
            type = list(_api[provider].keys())[type]  # TODO probably delete thhis because limits is in dict
        if isinstance(job_id, int) and provider is not None and type is not None:
            try:
                job_id = list(_api[provider][type].keys())[job_id]
            except IndexError:
                return ([], [], [])
        if all([isinstance(m, str) for m in [provider, type, job_id]]):
            job = _api.get(provider, {}).get(type, {}).get(job_id, None)
            return ([], [], []) if job is None else ([provider], [type], [job])

        # Prepare a list of all possible jobs
        providers, types, result = [], [], []
        if provider is None:
            for _provider in _api.keys():
                p, t, j = self.get_job(job_id, type, _provider)
                providers, types, result = providers + p, types + t, result + j
        else:
            provider = [provider]

        if type is None and provider is not None:
            for _provider in provider:
                for _type in [t for t in _api[_provider].keys() if
                              t != 'limits']:  # A provider could have different types of requests but limits is never one of them
                    p, t, j = self.get_job(job_id, _type, _provider)
                    providers, types, result = providers + p, types + t, result + j
        else:
            type = [type]

        if job_id is None and type is not None and provider is not None:
            for _type in type:
                for _provider in provider:
                    for _job_id in self.api[_provider][_type].keys():
                        p, t, j = self.get_job(_job_id, _type, _provider)
                        providers, types, result = providers + p, types + t, result + j

        return providers, types, result

    def prompts(self, job_id=None, type=None, provider=None):
        provider, type, job = self.get_job(job_id, type, provider)
        if job is None:
            return None
        if type == "chat":
            from .texts import Chat
            from .tensors import ChatTensor
            return ChatTensor([Chat.from_messages(*resp["messages"]) for resp in job["requests"]])
        elif type == "embeddings":
            from .tensors import TextTensor
            return TextTensor(self.extract_prompts(job["requests"]))

    def completions(self, job_id=-1, type=None, provider=None):
        self.order_responses(job_id, type, provider)
        provider, type, job = self.get_job(job_id, type, provider)
        result = []
        for p, t, j in zip(provider, type, job):
            if not j:
                pass
            if t == "chat":
                from .texts import Chat
                from .tensors import ChatTensor
                result += [[[Chat.from_messages(m['message']) for m in resp[1]["choices"]] for resp in entry] for entry
                           in j["responses"]]
            elif t == "embedding":
                import torch
                result += [torch.tensor([resp[1]["data"][0]["embedding"] for resp in entry]) for entry
                           in j["responses"]]
        return result

    def extract_prompts(self, dict_list):
        if dict_list is None: return None
        if isinstance(dict_list[0], list):
            dict_list = [m[0] for m in dict_list]
        return [(entry["input"] if "embedding" in entry else langtorch.Chat.from_messages(entry["messages"])) for entry
                in dict_list]

    def order_responses(self, job_id=None, type=None, provider=None):
        """Order all responses for a given job using keys or indexes, or order all resposnses"""
        # self.reload()
        provider, type, jobs = self.get_job(job_id, type, provider)
        for job in jobs:
            if isinstance(job, dict) and isinstance(next(iter(job["responses"])), list):
                requests_unordered, responses_unordered = tuple(job.get("responses", []))
                requests_ordered = self.extract_prompts(job.get("requests", []))

                ordered_responses = []
                try:
                    used_entries = []
                    for req_oredered in requests_ordered:
                        for i, (req, resp) in enumerate(zip(requests_unordered, responses_unordered)):
                            if req == req_oredered and i not in used_entries:
                                ordered_responses.append(resp)
                                used_entries.append(i)
                                break

                except Exception as e:
                    print(f"Error while ordering API responses: {e}")

                self.add_responses(provider, type, job_id, ordered_responses, override=True)
                return ordered_responses

    def __setattr__(self, name, value, save=True):
        if name in ["_config", "_temp", "_path", "_async_lock", "_thread_lock", "_open", "_override"]:
            # Use the base class's __setattr__ to prevent recursive calls
            super().__setattr__(name, value)
            if name == "_config" and self._path and save:
                OmegaConf.save(self._config, self._path)
        elif self._open and name.startswith('_'):
            # Set the attribute directly
            super().__setattr__(name, value)
        elif self._open:
            # Decompose the current configuration
            tensor_savepath = self._config.pop('tensor_savepath', None)
            tensors_metadata = self._config.pop('tensors', [])

            # Filter attributes starting with an underscore
            underscore_attrs = OrderedDict((k, v) for k, v in self._config.items() if k.startswith('_'))
            for k in underscore_attrs.keys():
                self._config.pop(k, None)

            self._config['tensor_savepath'] = tensor_savepath
            if isinstance(value, torch.Tensor):
                timestamp = datetime.datetime.now().isoformat()
                try:
                    tensors = torch.load(tensor_savepath)
                    tensors[name] = value
                    torch.save(tensors, tensor_savepath)
                except FileNotFoundError:
                    torch.save({name: value}, tensor_savepath)

                metadata = {
                    "id": name,
                    "object": str(type(value)),
                    "created": timestamp,
                    "shape": tuple(value.shape)
                }
                if name in [m["id"] for m in tensors_metadata]:
                    tensors_metadata = [m for m in tensors_metadata if m["id"] != name]
                self._config.tensors = list(tensors_metadata) + [metadata]
            else:
                self._config['tensors'] = tensors_metadata
                try:
                    if not name.startswith('_'):
                        self._config[name] = value
                        if name in [m["id"] for m in self._config["tensors"]]:
                            print(
                                f"Saving non-tensor with the same name as a saved tensor {name}, the tensor will be unobtainable (but remains saved)")
                    else:
                        underscore_attrs[name] = value

                except UnsupportedValueType:
                    raise UnsupportedValueType("Session can only fold primitive types and TextTenor objects.")

            # Merge underscore attributes at the end
            for k, v in underscore_attrs.items():
                self._config[k] = v

            if self._path and save:
                OmegaConf.save(self._config, self._path)
        else:
            raise RuntimeError("RuntimeError: Attempted to save attr in a closed session")

    @property
    def tensors(self):
        tensors = torch.load(self._config["tensor_savepath"])
        return tensors

    def __getattr__(self, name):
        # Load the latest configuration from the file
        # if self._path:
        #     print("LOAD")
        #     self._config = OmegaConf.load(self._path)

        if name in ["_config", "_path", "_async_lock", "_thread_lock", "_open"]:
            return super().__getattribute__(name)

        try:
            # This block of code seems intended to ensure that 'tensors' attribute exists
            # and initializes it if it doesn't, which should probably be handled elsewhere.
            _ = (self._config.tensors)
        except Exception:
            self.tensors = []

        # If the attribute name corresponds to an id in the tensors list, return that tensors
        if not hasattr(self._config, name) and name in [m["id"] for m in self._config["tensors"]]:
            return self.tensors[name]

        # Return the attribute from the configuration
        try:
            attr = self._config[name]
        except KeyError:
            if name in ["api"]:
                return dict()
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        return attr

    @classmethod
    def create_aliases(cls, aliases):
        for alias, path in aliases.items():
            def create_property(path):
                def property_func(self):
                    return getattr(self, path)

                return property(property_func)

            setattr(cls, alias, create_property(path))

    def __getitem__(self, entry):
        return self.__getattr__(entry)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __str__(self):
        return "---   Session Config   ---\n" + yaml.dump(
            OmegaConf.to_object(self._config)) + "---   --------------   ---\n"

    def _delete(self):
        # Cleanup: remove the session file
        os.remove(self._path)
        Session.current_session.set({})

    def save_memoization(self, module_spec, input_data, output_data):
        raise NotImplementedError
        key = hashlib.sha256(str(module_spec).encode() + str(input_data).encode()).hexdigest()
        entry = {
            "module_spec": module_spec,
            "input": input_data,
            "output": output_data
        }
        self.config['memoization'][key] = entry

    def load_memoization(self, module_spec, input_data):
        raise NotImplementedError
        key = hashlib.sha256(str(module_spec).encode() + str(input_data).encode()).hexdigest()
        return self.config['memoization'].get(key, None)

    def get_tensor_metadata(self):
        raise NotImplementedError


ctx = Session()
ctx.create_aliases(cfg_yaml_aliases)
