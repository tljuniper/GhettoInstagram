#!/usr/bin/env python3

import os
from datetime import datetime
import uuid

CWD = os.path.abspath(os.getcwd())
STORAGE = os.path.join(CWD, "storage")


def generateUniquePath(pathname, extension):
    uniqueFilepath = pathname + str(uuid.uuid4()) + extension
    if os.path.exists(uniqueFilepath):
        return generateUniquePath(pathname, extension)
    return uniqueFilepath


def getPath(user, extension):
    userPath = os.path.join(STORAGE, user)
    userExists = os.path.exists(userPath)

    if not userExists:
        os.makedirs(userPath)

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S")

    photoPath = os.path.join(userPath, timestampStr)

    uniquePath = generateUniquePath(photoPath, extension)

    return uniquePath
