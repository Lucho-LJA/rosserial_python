#!/usr/bin/env python

#####################################################################
# Software License Agreement (BSD License)
#
# Copyright (c) 2020, Luis Allauca, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__author__ = "ljallauca.a@gmail.com (Luis Allauca)"

import rospy
from rosserial_python import SerialClient, RosSerialServer
from serial import SerialException
from time import sleep
import multiprocessing

import sys

if __name__=="__main__":

    rospy.init_node("wifi_rasp_node")
    rospy.loginfo("ROS Serial WIFI Python Node")

    port_name = rospy.get_param('~port','/dev/ttyUSB0')
    baud = int(rospy.get_param('~baud','115200'))

    # for systems where pyserial yields errors in the fcntl.ioctl(self.fd, TIOCMBIS, \
    # TIOCM_DTR_str) line, which causes an IOError, when using simulated port
    fix_pyserial_for_test = rospy.get_param('~fix_pyserial_for_test', False)

    # TODO: should these really be global?
    tcp_portnum = int(rospy.get_param('/rosserial_embeddedlinux/tcp_port', '11423'))
    fork_server = rospy.get_param('/rosserial_embeddedlinux/fork_server', False)

    # TODO: do we really want command line params in addition to parameter server params?
    sys.argv = rospy.myargv(argv=sys.argv)
    if len(sys.argv) == 2 :
        tcp_portnum  = sys.argv[1]
    server = RosSerialServer(tcp_portnum, fork_server)
    rospy.loginfo("Waiting for socket connections on port %d" % tcp_portnum)
    try:
        server.listen()
    except KeyboardInterrupt:
        rospy.loginfo("got keyboard interrupt")
    finally:
        rospy.loginfo("Shutting down")
        for process in multiprocessing.active_children():
            rospy.loginfo("Shutting down process %r", process)
            process.terminate()
            process.join()
            rospy.loginfo("All done")


