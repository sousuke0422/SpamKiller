import re
from idna import encode, decode

# use chatgpt
# 書き直したいけど、動いてるので `触らぬ神に祟りなし`
def convert_punycode_to_unicode(input_string: str) -> str:
    # 正規表現を使用して文字列からPunycodeを抽出
    punycode_matches = re.findall(r'xn--[a-zA-Z0-9]+', input_string)

    # 各PunycodeをUnicodeに変換
    for punycode_match in punycode_matches:
        unicode_domain = decode(punycode_match).encode('utf-8').decode('utf-8')
        input_string = input_string.replace(punycode_match, unicode_domain)

    return input_string

#input_string = "This is a punycode example: xn--fsq@xn--fsq.com"
#converted_string = convert_punycode_to_unicode(input_string)
#print(converted_string)
