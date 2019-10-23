from eth_utils import remove_0x_prefix

def hex2a(s):
    # astr = ''
    chrlist = []
    s = remove_0x_prefix(s)
    for i in range(0, len(s), 2):
        aint = int(s[i:i + 2], 16)
        if aint >= 32:
            # astr = astr + chr(aint)
            chrlist.append(aint)
    return ''.join(map(chr, chrlist))
