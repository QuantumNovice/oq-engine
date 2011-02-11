# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
Tests for the Python-Java code layer.
"""

import jpype
import os
import unittest

from mock import Mock
from openquake import java


class JvmMaxMemTestCase(unittest.TestCase):
    """Tests related to the JVM's maximum memory setting"""

    def test_jvm_setup_without_maxmem_environ_var_and_param(self):
        """
        If the OQ_JVM_MAXMEM environment variable is not set and the 'max_mem'
        parameter is not passed the default value should be used when starting
        the JVM.
        """

    def test_jvm_setup_without_maxmem_environ_var_but_with_param(self):
        """
        If the OQ_JVM_MAXMEM environment variable is not set and the 'max_mem'
        parameter is passed its value should be used when starting the JVM.
        """

    def test_jvm_setup_honours_maxmem_environ_var(self):
        """
        The value of the OQ_JVM_MAXMEM environment variable is honoured
        when starting the JVM.
        """
