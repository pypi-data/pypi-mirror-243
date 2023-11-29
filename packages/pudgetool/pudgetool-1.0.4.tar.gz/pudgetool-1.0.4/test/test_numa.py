#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
from __future__ import print_function
from Cython.Build import cythonize
import pytest
import os

class TestNuma():
    def __init__(self):
        # 编译 Cython 扩展  
        pyx_file = 'numa.pyx'  # 您的 Cython 文件名  
        abs_path = os.getcwd()
        pack_file = os.path.join(abs_path, pyx_file)
        numa_ext = cythonize(pack_file)
      
        # 验证扩展是否成功构建  
        assert numa_ext is not None  
        assert isinstance(numa_ext.__dict__['numa'], type)  
            
        # 测试扩展中的函数或方法  
        my_instance = numa_ext.MyClass(42)  
        assert my_instance.value == 42
    

    def test_available(self):
        assert True == sys.available()

    def test_node_size(self):
        for node in range(sys.get_max_node()+1):
            print('Node: %d, size: %r' % (node, sys.get_node_size(node)))

    def test_preferred(self):
        print('Preferred node:', sys.get_preferred())

    def test_node_to_cpus(self):
        print('Node CPUs:', sys.node_to_cpus(sys.get_preferred()))

    def test_nodemask(self):
        if not hasattr(sys, 'set_to_numa_nodemask'):
            raise pytest.SkipTest("skipped for Cython")

        assert set([0]) == sys.numa_nodemask_to_set(sys.set_to_numa_nodemask(set([0])))

    def test_interleave(self):
        sys.set_interleave_mask(set([0]))
        assert set([0]) == sys.get_interleave_mask()

    def test_zz_bind(self):
        # conflicts with test_node_to_cpus
        sys.bind(set([0]))

    def test_set_preferred(self):
        sys.set_preferred(0)

    def test_localalloc(self):
        sys.set_localalloc()

    def test_membind(self):
        sys.set_membind([0])
        pytest(set([0]), sys.get_membind())

    def test_run_on_nodemask(self):
        sys.set_run_on_node_mask(set([0]))
        assert set([0]) == sys.get_run_on_node_mask()

    def test_get_distance(self):
        assert 10 == sys.get_distance(0, 0)

    def test_affinity(self):
        sys.set_affinity(0, set([0]))
        assert set([0]) == sys.get_affinity(0)

if __name__ == '__main__':
    pytest.main()