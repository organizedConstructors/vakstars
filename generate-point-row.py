#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if len(sys.argv) == 8:
  if sys.argv[1] == "+":
    points_to_sender = 2
    points_to_receiver = 10
  else:
    points_to_sender = -2
    points_to_receiver = -1
  sender_new_points = int(sys.argv[3]) + points_to_sender
  receiver_new_points = int(sys.argv[5]) + points_to_receiver
  print '<tr><td>{date}</td>' \
          '<td>{type}</td>' \
          '<td>{sender} ' \
          '({from_points_before} &rarr; {from_points_after})</td>' \
          '<td>{receiver} ' \
          '({to_points_before} &rarr; {to_points_after})</td>' \
          '<td>{reason}</td></tr>'.format(
          date=sys.argv[7], type=sys.argv[1], sender=sys.argv[2], \
          from_points_before=sys.argv[3], \
          from_points_after=sender_new_points, \
          receiver=sys.argv[4], \
          to_points_before=sys.argv[5], \
          to_points_after=receiver_new_points, \
          reason=sys.argv[6])
else:
  print "<+|-> <Küldő> <Küldő pontszáma> <Fogadó> <Fogadó pontszáma> <Indoklás> <Dátum>"
