import base64

def file_to_string(file_path):
    with open(file_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return encoded

def generate_nbt_file( output_path):
    encoded_str=s
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(encoded_str.encode('utf-8')))

# 序列化
s = ('H4sIAFIVBmgA/9VSwWoTURQ96UyayRTBheCui+AHdN1trOBGgxS38jK5HR+dzhveezFGUSxSSRBpiy6EIBQXQpVQxYVFAv2ZvCZZ9Rd6J2'
     '0hQvMBLi7vXu495zw4JwTK8I18QR6AvApXVcZiPVHRpgnzyUPRWGGJe0Z4mTJXAFwCEMJL6zaEf9/SVoAF2cDNSBODVqNEZnUldINvrIg9'
     '3KppeiZV0yTthxml1KiJ+JK7mLcXomWU1lKr5cUYFFCqPqVokxoI4K/Tc4vllxXLb2W1ctrZP/18NDz+7r7suv6h6++9rrzCNZCVWcjZoD'
     'M8/uB+7rqTt2eDruv8Gf595zq9yZuDUffQfdyeQ3JnlmT8bXv89Yfb+T0+6Y16+6P3v5hkDvD2LHAyOJh86vPxf3jL3vvr7Yym7hdQrKpm'
     'agscgvI9pWOqisxgTghyl0uZSMhamvrMYg/EFl0Xl7CmVUbacgYCLLV4qxMVx/zD4oZIDAVY3BCRTGP4JIxlJh6Jl4lSOkCppSWrpPCtbl'
     'IuHFBqZU43zayHpbvCisekjVQpcKPL2XwkZNISbfPknxUWcA4wN6m3LgMAAA==')

if __name__ == '__main__':
    generate_nbt_file( "chanhuishu.nbt")