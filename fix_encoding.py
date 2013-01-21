import codecs, eyeD3, sys

def strip_unicode(text):
  text_repr = repr(text)
  if text_repr.startswith("u"):
    text_repr = text_repr[1:]
  stripped_text = eval(text_repr)
  return stripped_text


def decode_text(text, encoding="cp1251"):
  try:
    fixed_text = codecs.decode(text, encoding)
    return fixed_text
  except:
    print 'Could not decode', [ text ]
    return None


def is_cp1251(text):
  text_repr = repr(unicode(text))
  if '\\x' in text_repr:
    if '\\u' in text_repr:
      print 'Found both markers in', text_repr
      sys.exit(1)
    return True
  return False


def fix_tag(filename):
  tag = eyeD3.Tag()
  tag.link(filename)
  tag.setVersion(eyeD3.ID3_V2_4)
  tag.setTextEncoding(eyeD3.UTF_8_ENCODING)
  
  for frame in tag.frames:
    if frame.__class__ is eyeD3.frames.TextFrame:
      new_string = ''
      for text_byte in frame.text:
        if is_cp1251(text_byte):
          decoded_byte = decode_text(strip_unicode(text_byte))
          if decoded_byte:
            if repr(decoded_byte) != repr(text_byte):
              new_string += decoded_byte
              continue
        # No decoded byte to append.
        new_string += text_byte
      if repr(frame.text) != repr(new_string):
        frame.text = new_string
 
  tag.update()
  print 'Fixed', filename


def fix_files(filenames):
  for filename in filenames:
    filename = filename.strip()
    if not filename.endswith(".mp3"):
      continue

    fix_tag(filename) 


if __name__ == "__main__":
  fix_files(sys.stdin.readlines())
