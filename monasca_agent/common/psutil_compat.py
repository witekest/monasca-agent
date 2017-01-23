# (C) Copyright 2017 Fujitsu Limited
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import psutil

from collections import namedtuple


sconn = namedtuple('sconn', ['fd', 'family', 'type', 'laddr', 'raddr',
                             'status', 'pid'])


def cpu_count(logical=True):
    try:
        return psutil.cpu_count(logical)
    except AttributeError:
        if logical:
            return psutil.NUM_CPUS
        else:
            raise NotImplementedError


def cpu_times(percpu=False):
    return psutil.cpu_times(percpu)


def cpu_percent(interval=None, percpu=False):
    return psutil.cpu_percent(interval, percpu)


def cpu_times_percent(interval=None, percpu=False):
    return psutil.cpu_times_percent(interval, percpu)


def net_connections(kind='inet'):
    try:
        return psutil.net_connections(kind)
    except AttributeError:
        ret = set()
        for p in process_iter():
            try:
                for c in p.connections(kind):
                    conn = sconn(c.fd, c.family, c.type, c.laddr, c.raddr,
                                 c.status, p.psutil_proc.pid)
                    ret.add(conn)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
        return list(ret)


def process_iter():
    for p in psutil.process_iter():
        yield Process(process=p)


class Process(object):

    def __init__(self, pid=None, process=None):
        if process:
            self.psutil_proc = process
        else:
            self.psutil_proc = psutil.Process(pid)

    def connections(self, kind='inet'):
        try:
            return self.psutil_proc.connections(kind)
        except AttributeError:
            return self.psutil_proc.get_connections(kind)

    def cpu_affinity(self, cpus=None):
        try:
            return self.psutil_proc.cpu_affinity(cpus)
        except AttributeError:
            return self.psutil_proc.get_cpu_affinity()

    def cpu_percent(self, interval=None):
        try:
            return self.psutil_proc.cpu_percent(interval)
        except AttributeError:
            return self.psutil_proc.get_cpu_percent(interval)

    def cpu_times(self):
        try:
            return self.psutil_proc.cpu_times()
        except AttributeError:
            return self.psutil_proc.get_cpu_times()

    def memory_info_ex(self):
        try:
            return self.psutil_proc.memory_info_ex()
        except AttributeError:
            return self.psutil_proc.get_ext_memory_info()

    def io_counters(self):
        try:
            return self.psutil_proc.io_counters()
        except AttributeError:
            return self.psutil_proc.get_io_counters()

    def ionice(self, ioclass=None, value=None):
        try:
            return self.psutil_proc.ionice(ioclass, value)
        except AttributeError:
            return self.psutil_proc.get_ionice()

    def memory_info(self):
        try:
            return self.psutil_proc.memory_info()
        except AttributeError:
            return self.psutil_proc.get_memory_info()

    def memory_maps(self, grouped=True):
        try:
            return self.psutil_proc.memory_maps(grouped)
        except AttributeError:
            return self.psutil_proc.get_memory_maps(grouped)

    def memory_percent(self):
        try:
            return self.psutil_proc.memory_percent()
        except AttributeError:
            return self.psutil_proc.get_memory_percent()

    def nice(self, value=None):
        try:
            return self.psutil_proc.nice(value)
        except AttributeError:
            return self.psutil_proc.get_nice(value)

    def num_ctx_switches(self):
        try:
            return self.psutil_proc.num_ctx_switches()
        except AttributeError:
            return self.psutil_proc.get_num_ctx_switches()

    def num_fds(self):
        try:
            return self.psutil_proc.num_fds()
        except AttributeError:
            return self.psutil_proc.get_num_fds()

    def num_threads(self):
        try:
            return self.psutil_proc.num_threads()
        except AttributeError:
            return self.psutil_proc.get_num_threads()

    def open_files(self):
        try:
            return self.psutil_proc.open_files()
        except AttributeError:
            return self.psutil_proc.get_open_files()

    def rlimit(self, resource, limits=None):
        try:
            return self.psutil_proc.rlimit(resource, limits)
        except AttributeError:
            return self.psutil_proc.get_rlimit(resource)

    def threads(self):
        try:
            return self.psutil_proc.threads()
        except AttributeError:
            return self.psutil_proc.get_threads()

    def cwd(self):
        try:
            return self.psutil_proc.cwd()
        except AttributeError:
            return self.psutil_proc.getcwd()

    def name(self):
        try:
            return self.psutil_proc.name()
        except TypeError:
            return self.psutil_proc.name

    def cmdline(self):
        try:
            return self.psutil_proc.cmdline()
        except TypeError:
            return self.psutil_proc.cmdline

    def exe(self):
        return self.psutil_proc.exe()
