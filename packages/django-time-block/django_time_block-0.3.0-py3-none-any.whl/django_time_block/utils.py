#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
utils to handle the time block
"""


from dataclasses import dataclass

import datetime
import logging

from typing import Optional

from .models import TimeBlock


LOGGER = logging.getLogger(__name__)


@dataclass
class Duration:
    start: datetime.datetime
    end: datetime.datetime


def add_time_block(object_id: str, duration: Duration):
    """
    first scenerio:
        the old time block contains new timeblock
        ===========  old time
          ----       new time

    second scenerio:
        ==== == ====  old time
          -------     new time

    third scenerio:
        ====     ===  old time
             ---      new time
    """
    # first sceneraio
    start_datetime = duration.start
    end_datetime = duration.end
    LOGGER.debug("add time block %s [%s~%s)", object_id, start_datetime, end_datetime)
    queryset = TimeBlock.objects.filter(object_id=object_id).order_by("start_datetime")
    if queryset.filter(
            start_datetime__lte=start_datetime,
            end_datetime__gte=end_datetime).exists():
        LOGGER.debug("time already exist")
        return
    new_timeblock = TimeBlock.objects.create(
            object_id=object_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime
    )
    # merge the overlap timeblock
    queryset.filter(
            start_datetime__gte=new_timeblock.start_datetime,
            end_datetime__lte=new_timeblock.end_datetime,
    ).exclude(id=new_timeblock.id).delete()
    # pylint: disable=pointless-string-statement
    """
    now, there is not time block in the new time, we can extend the front overlap
    and end overlap timeblock
    =======     ========  old time
         ---------        new time
         |      |
       front    |
      overlap   |
               end
             overlap
    """
    front_overlap = queryset.filter(
            start_datetime__lt=new_timeblock.start_datetime,
            end_datetime__gte=new_timeblock.start_datetime,
    ).first()
    if front_overlap:
        front_overlap.end_datetime = new_timeblock.end_datetime
        front_overlap.save()
    end_overlap = queryset.filter(
            start_datetime__lte=new_timeblock.end_datetime,
            end_datetime__gt=new_timeblock.end_datetime,
    )
    if end_overlap:
        end_overlap.start_datetime = new_timeblock.start_datetime
        end_overlap.save()
    if front_overlap or end_overlap:
        new_timeblock.delete()
    if front_overlap and end_overlap:
        front_overlap.end_datetime = end_overlap.end_datetime
        front_overlap.save()
        end_overlap.delete()


def all_include(object_id: str, duration: Duration) -> bool:
    """
    check if a duration is included
    """
    return TimeBlock.objects.filter(
        object_id=object_id,
        start_datetime__lte=duration.start,
        end_datetime__gte=duration.end,
    ).exists()


def find_min_uninclude(object_id: str, duration: Duration) -> datetime.datetime:
    """
    find the min datetime that was not included
    =====      ====  old time
     ---             case 0
        ---          case 1
          ---        case 2
            ----     case 3
      -----------    also case 3
    """
    if all_include(object_id, duration):
        return None
    old_time_block = TimeBlock.objects.filter(
            object_id=object_id,
            start_datetime__lte=duration.start
    ).order_by("start_datetime").last()
    if old_time_block:
        return max(
            old_time_block.end_datetime,
            duration.start)
    return duration.start


def find_max_uninclude(object_id, duration) -> Optional[datetime.datetime]:
    """
    find the max datetime that was not included
    =====      ====  old time
     ---             case 0
        ---          case 1
          ---        case 2
            ----     case 3
      -----------    also case 3
    """
    # case 0
    if all_include(object_id, duration):
        return None
    # case 3
    block = TimeBlock.objects.filter(
        object_id=object_id,
        end_datetime__lte=duration.end
    ).order_by("end_datetime").first()
    if block:
        return min(
            block.start_datetime,
            duration.end
        )
    # case 1,2
    return duration.end
