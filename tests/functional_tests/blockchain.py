#!/usr/bin/env python3

# Copyright (c) 2018 The Monero Project
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# Parts of this file are originally copyright (c) 2014-2016 The Bitcoin Core developers

"""Test RPCs related to blockchainstate.

Test the following RPCs:
    - get_info

Tests correspond to code in ...
"""

from decimal import Decimal
import http.client
import subprocess
import sys
import time

from test_framework.util import (
    assert_equal,
    assert_greater_than,
    assert_greater_than_or_equal,
    assert_raises,
    assert_raises_rpc_error,
    assert_is_hex_string,
    assert_is_hash_string,
)

from monero.daemon import Daemon
from monero.backends.jsonrpc import JSONRPCDaemon


class BlockchainTest():
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        self._test_get_info()
        self._test_generateblocks(5)

    def _test_get_info(self):
        print("Test get_info")

        keys = [
                'alt_blocks_count', 
                'block_size_limit', 
                'block_size_median', 
                'bootstrap_daemon_address', 
                'cumulative_difficulty', 
                'difficulty', 
                'free_space', 
                'grey_peerlist_size', 
                'height', 
                'height_without_bootstrap', 
                'incoming_connections_count', 
                'nettype', 
                'offline', 
                'outgoing_connections_count', 
                'rpc_connections_count', 
                'start_time', 
                'status', 
                'target', 
                'target_height', 
                'top_block_hash', 
                'tx_count', 
                'tx_pool_size', 
                'untrusted', 
                'was_bootstrap_ever_used', 
                'white_peerlist_size'
                ]

        daemon = Daemon(JSONRPCDaemon(port=28081))
        res = daemon.info()

        assert_equal(sorted(res.keys()), sorted(keys))

        # free_space should be > 0
        assert_greater_than(res['free_space'], 0)

        # height should be greater or equal to 0
        assert_greater_than_or_equal(res['height'], 0)

    def _test_generateblocks(self, blocks):
        print("Test generating", blocks, "blocks")
        daemon = Daemon(JSONRPCDaemon(port=28081))
        res = daemon.info()
        height = res['height']

        res = daemon._backend.raw_jsonrpc_request('generateblocks', {
            'amount_of_blocks' : blocks,
            'reserve_size' : 20,
            'wallet_address': '4RnWk1VMxP4XS82k2ovp5EUYLzBt9pYNW2LXUFsZiv8S3Mt21FZ5qQaAroko1enzw3eGr9qC7X1D7Geoo2RrAotYPyUsZ7F'})
        
        res = daemon.info()
        assert_equal(res['height'], height + blocks)
        

if __name__ == '__main__':
    BlockchainTest().run_test()
