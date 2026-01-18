import pysrt

def read_srt_file(srt_file):
  
  
  subs = pysrt.open(srt_file, encoding="utf-8")

  sentence_groups = []

  for sub in subs:
      sentence_groups.append({
          "start": sub.start.ordinal / 1000,  # seconds
          "end": sub.end.ordinal / 1000,      # seconds
          "text": sub.text.replace("\n", " ")
      })
  
  return sentence_groups