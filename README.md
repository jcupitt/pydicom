# pydicom

This is a tiny, experimental binding for
[libdicom](https://github.com/jcupitt/libdicom) to validate the API. It
is not supposed to be ready for production! There are plenty of obvious
missing features and useful enhancements.

Having said that, it does work, performs well, has no memory leaks (I
think), and supports the whole libdicom file read API.

# Sample code

```python
file = pydicom.Filehandle.create_from_file("sm_image.dcm")
metadata = file.get_metadata()
num_frames_tag = pydicom.Tag.create_from_keyword("NumberOfFrames")
num_frames = int(metadata.get(num_frames_tag).get_value()[0])
for frame_number in range(1, num_frames + 1):
    frame = file.read_frame(frame_number)
    value = frame.get_value()
    print(f"frame {frame_number} -> {frame} {len(value)} bytes")
```
