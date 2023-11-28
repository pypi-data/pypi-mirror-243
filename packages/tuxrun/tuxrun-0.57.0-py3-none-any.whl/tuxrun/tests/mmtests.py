# vim: set ts=4
#
# Copyright 2023-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test
import re


class MMTests(Test):
    devices = ["qemu-arm64", "qemu-x86_64"]
    configfile: str = ""
    iterations: int = 0
    need_test_definition = True

    def render(self, **kwargs):
        kwargs["name"] = self.name
        kwargs["configfile"] = self.configfile
        kwargs["iterations"] = self.iterations
        kwargs["timeout"] = self.timeout
        return self._render("mmtests.yaml.jinja2", **kwargs)


class MMTestsDbSqliteInsertSmall(MMTests):
    configfile = "configs/config-db-sqlite-insert-small"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsHpcScimarkcSmall(MMTests):
    configfile = "configs/config-hpc-scimarkc-small"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 20
    timeout = 90


class MMTestsBlogbench(MMTests):
    configfile = "configs/config-io-blogbench"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 30
    timeout = 90


class MMTestsFioRandreadAsyncRandwrite(MMTests):
    configfile = "configs/config-io-fio-randread-async-randwrite"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsFioRandreadAsyncSeqwrite(MMTests):
    configfile = "configs/config-io-fio-randread-async-seqwrite"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsFioRandreadSyncHeavywrite(MMTests):
    configfile = "configs/config-io-fio-randread-sync-heavywrite"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsFioRandreadSyncRandwrite(MMTests):
    configfile = "configs/config-io-fio-randread-sync-randwrite"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsFsmarkSmallFileStream(MMTests):
    configfile = "configs/config-io-fsmark-small-file-stream"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsRedisBenchmarkSmall(MMTests):
    configfile = "configs/config-memdb-redis-benchmark-small"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 20
    timeout = 90


class MMTestsRedisMemtierSmall(MMTests):
    configfile = "configs/config-memdb-redis-memtier-small"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 20
    timeout = 90


class MMTestsSchbench(MMTests):
    configfile = "configs/config-scheduler-schbench"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsSysbenchCpu(MMTests):
    configfile = "configs/config-scheduler-sysbench-cpu"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsSysbenchThread(MMTests):
    configfile = "configs/config-scheduler-sysbench-thread"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsCoremark(MMTests):
    configfile = "configs/config-workload-coremark"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 20
    timeout = 90


class MMTestsCyclictestFineHackbench(MMTests):
    configfile = "configs/config-workload-cyclictest-fine-hackbench"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 15
    timeout = 90


class MMTestsCyclictestHackbench(MMTests):
    configfile = "configs/config-workload-cyclictest-hackbench"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 20
    timeout = 90


class MMTestsEbizzy(MMTests):
    configfile = "configs/config-workload-ebizzy"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsPmqtestHackbench(MMTests):
    configfile = "configs/config-workload-pmqtest-hackbench"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsStressngClassIoParallel(MMTests):
    configfile = "configs/config-workload-stressng-class-io-parallel"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsStressngContext(MMTests):
    configfile = "configs/config-workload-stressng-context"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsStressngGet(MMTests):
    configfile = "configs/config-workload-stressng-get"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsStressngMmap(MMTests):
    configfile = "configs/config-workload-stressng-mmap"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90


class MMTestsUsemem(MMTests):
    configfile = "configs/config-workload-usemem"
    name = re.sub(r"configs/config-", "mmtests-", configfile)
    iterations = 10
    timeout = 90
