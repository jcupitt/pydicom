#!/usr/bin/env python

import pydicom

print(f"testing Tag ...")
tag = pydicom.Tag.create_from_keyword("NumberOfFrames")
print(f"NumberOfFrames = {tag}")
print(f"tag.keyword() = {tag.keyword()}")

print(f"testing bad Tag ...")
try:
    tag = pydicom.Tag.create_from_keyword("poop")
except Exception as e:
    print(f"expected failure, exception is:")
    print(f"  {e}")

print(f"testing VR ...")
vr = pydicom.VR.create_from_name("SQ")
print(f"create_from_name('SQ') = {vr}")

print(f"testing bad VR ...")
try:
    vr = pydicom.VR.create_from_name("banana")
except Exception as e:
    print(f"expected failure, exception is:")
    print(f"  {e}")

print(f"testing create_from_file ...")
file = pydicom.Filehandle.create_from_file("sm_image.dcm")
print(f"file = {file}")

print(f"testing create_from_file error handling ...")
try:
    file = pydicom.Filehandle.create_from_file("banana.dcm")
except Exception as e:
    print(f"expected failure, exception is:")
    print(f"  {e}")

def print_sequence(seq, indent=0):
    for index in range(0, seq.count()):
        print(f"{' '*indent}-- Item #{index} --")
        print_dataset(seq.get(index), indent + 2)

def print_dataset(dataset, indent=0):
    for tag in dataset.tags():
        element = dataset.get(tag)
        print(f"{' '*indent}{element}")
        if element.vr_class() == pydicom.VRClass.SEQUENCE:
            seq = element.get_value()
            print_sequence(seq, indent + 2)

print(f"testing get_file_meta ...")
file_meta = file.get_file_meta()
print(f"file_meta = {file_meta}")
tags = file_meta.tags()
print(f"tags = {tags}")
print(f"contains(tags[0]) = {file_meta.contains(tags[0])}")
print_dataset(file_meta)

print(f"testing get_metadata ...")
metadata = file.get_metadata()
print(f"metadata = {metadata}")
tags = metadata.tags()
print(f"tags = {tags}")
print(f"contains(tags[0]) = {metadata.contains(tags[0])}")
print_dataset(metadata)



