
def strip_list(list):
  i = 0
  count = len(list)
  while i < count:
      list[i] = list[i].strip()
      i += 1

def verbose_timer(t1,t2): 
    delta = t2-t1
    seconds = delta.total_seconds()
    print("Seconds: " + str(seconds));
    if (seconds>60):
        print("Minutes: " + str(seconds/60));
    if (seconds>3600):
        print("Hours: " + str(seconds/3600));
    if (seconds>3600*24):   
        print("Days: " + str(seconds/(3600*24)));

def get_seconds(t1,t2):
    delta = t2-t1
    seconds = delta.total_seconds()
    return seconds


ENC = "utf-8"

def trunc_str(src, trunc_at, om = ""):
    # https://gist.github.com/komasaru/b25cbdf754971f920dd2f5743e950c7d
    str_size, str_bytesize = len(src), len(src.encode(ENC))
    om_size = (len(om.encode(ENC))- len(om)) // 2 + len(om)
    if str_size == str_bytesize:
        if str_size <= trunc_at:
            return src
        else:
            return src[:(trunc_at - om_size)] + om
    if (str_bytesize - str_size) // 2 + str_size <= trunc_at:
        return src
    for i in range(str_size):
        s = (len(src[:(i + 1)].encode(ENC)) - len(src[:(i + 1)])) // 2 \
          + len(src[:(i + 1)])
        if s < trunc_at - om_size:
            continue
        elif s == trunc_at - om_size:
            return src[:(i + 1)] + om
        else:
            return src[:i] + om
    return src