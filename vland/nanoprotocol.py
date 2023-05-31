PKG_HEAD_BYTES = 4
MSG_FLAG_BYTES = 1
MSG_ROUTE_CODE_BYTES = 2
MSG_ID_MAX_BYTES = 5
MSG_ROUTE_LEN_BYTES = 1

MSG_ROUTE_CODE_MAX = 0xffff

MSG_COMPRESS_ROUTE_MASK = 0x1
MSG_TYPE_MASK = 0x7
MSG_TYPE_ZIP = 0x1

class Protocol:
    # 将字符串转换为字节数组
    def strencode(s):
        # 创建一个字节数组，长度为字符串长度的三倍
        byte_array = bytearray(len(s) * 3)
        offset = 0
        # 遍历字符串中的每个字符
        for i in range(len(s)):
            char_code = ord(s[i]) # 获取字符的ASCII码值
            codes = None
            # 根据ASCII码值的范围将字符转换为字节数组
            if char_code <= 0x7f:
                codes = [char_code]
            elif char_code <= 0x7ff:
                codes = [0xc0 | (char_code >> 6), 0x80 | (char_code & 0x3f)]
            else:
                codes = [
                    0xe0 | (char_code >> 12),
                    0x80 | ((char_code & 0xfc0) >> 6),
                    0x80 | (char_code & 0x3f),
                ]
            # 将字节数组中的每个元素逐个复制到新的字节数组中
            for j in range(len(codes)):
                byte_array[offset] = codes[j]
                offset += 1
        # 创建一个新的字节数组，长度为offset
        buffer = bytearray(offset)
        buffer[0:offset] = byte_array[0:offset] # 复制字节数组
        return buffer
    
    # 将字节数组转换为字符串
    def strdecode(buffer):
        # 将输入的buffer转换为ByteArray类型
        bytes = bytearray(buffer)
        array = []
        offset = 0
        charCode = 0
        # 获取bytes的长度
        end = len(bytes)
        # 循环遍历bytes
        while offset < end:
            # 如果当前字节小于128, 字符编码为当前字节
            if bytes[offset] < 128:
                charCode = bytes[offset]
                offset += 1
            # 如果当前字节大于等于128且小于224, 字符编码为当前字节的后6位左移6位加上下一个字节的后6位
            elif bytes[offset] < 224:
                charCode = ((bytes[offset] & 0x3f) << 6) + (bytes[offset + 1] & 0x3f)
                offset += 2
            # 如果当前字节大于等于224, 字符编码为当前字节的后4位左移12位加上下一个字节的后6位左移6位再加上下下个字节的后6位
            else:
                charCode = ((bytes[offset] & 0x0f) << 12) + ((bytes[offset + 1] & 0x3f) << 6) + (bytes[offset + 2] & 0x3f)
                offset += 3
            # 将字符编码添加到数组中
            array.append(charCode)
        return ''.join([chr(i) for i in array])
    
    class Package: 
        TYPE_HANDSHAKE = 1
        TYPE_HANDSHAKE_ACK = 2
        TYPE_HEARTBEAT = 3
        TYPE_DATA = 4
        TYPE_KICK = 5
        TYPE_API = 6

        # 将数据包编码为字节数组
        def encode(type, body):
            # 计算body长度
            length = len(body) if body else 0
            # 创建一个字节数组，长度为PKG_HEAD_BYTES + body长度
            buffer = bytearray(PKG_HEAD_BYTES + length)
            index = 0
            # 将type写入buffer中
            buffer[index] = type & 0xff
            index += 1
            # 将body长度写入buffer中
            buffer[index] = (length >> 16) & 0xff
            index += 1
            buffer[index] = (length >> 8) & 0xff
            index += 1
            buffer[index] = length & 0xff
            index += 1
            # 如果body不为空，则将其写入buffer中
            if body:
                buffer[index:index+length] = body[:]
            return buffer
        
        # 将字节数组解码为数据包
        def decode(buffer):
            offset = 0
            bytes = bytearray(buffer)
            length = 0
            rs = []
            while offset < len(bytes):
                # 从buffer中读取type
                type = bytes[offset]
                offset += 1
                # 从buffer中读取body长度
                length = ((bytes[offset] << 16) | (bytes[offset+1] << 8) | bytes[offset+2]) & 0xffffffff
                offset += 3
                # 如果body长度不为0，则从buffer中读取body
                body = bytes[offset:offset+length] if length > 0 else None
                offset += length
                # 将type和body封装成一个字典并加入rs列表中
                rs.append({'type': type, 'body': body})
            # 如果rs列表长度为1，则直接返回字典；否则返回rs列表
            return rs[0] if len(rs) == 1 else rs

    class Message: 
        TYPE_REQUEST = 0
        TYPE_NOTIFY = 1
        TYPE_RESPONSE = 2
        TYPE_PUSH = 3

        def encode(id, type, compressRoute, route, msg, zip=False):
            # 计算消息最大长度
            idBytes = caculateMsgIdBytes(id) if msgHasId(type) else 0
            msgLen = MSG_FLAG_BYTES + idBytes

            

            if msgHasRoute(type):
                

                if compressRoute:
                    if not isinstance(route, int):
                        raise ValueError("error flag for number route!")
                    msgLen += MSG_ROUTE_CODE_BYTES
                else:
                    msgLen += MSG_ROUTE_LEN_BYTES
                    if route:
                        route = Protocol.strencode(route)
                        if len(route) > 255:
                            raise ValueError("route maxlength is overflow")
                        msgLen += len(route)


            if msg:
                # print(msg, msgLen)
                msgLen += len(msg)
                
        
            buffer = bytearray(msgLen)
            offset = 0

            # 添加flag标志
            offset = encodeMsgFlag(type, compressRoute, buffer, offset, zip)

            # 添加消息id
            if msgHasId(type):
                offset = encodeMsgId(id, buffer, offset)

            # 添加路由
            if msgHasRoute(type):
                offset = encodeMsgRoute(compressRoute, route, buffer, offset)

            # 添加消息体
            if msg:
                offset = encodeMsgBody(msg, buffer, offset)

            # print("Message 返回的buffer", buffer,  len(buffer))

            return buffer
        
        def decode(buffer):
            # 创建一个字节数组
            bytes = bytearray(buffer)
            bytesLen = len(bytes)

            offset = 0
            id = 0
            route = None

            # 解析flag
            flag = bytes[offset]
            offset += 1
            # 获取压缩路由的标志位
            compressRoute = flag & MSG_COMPRESS_ROUTE_MASK
            # 获取消息类型
            type = (flag >> 1) & MSG_TYPE_MASK
            # 获取是否压缩的标志位
            zip = (flag >> 4) & MSG_TYPE_ZIP

            # 解析id
            

            if msgHasId(type):
                m = int(bytes[offset])
                
                i = 0
                while m >= 128:
                    m = int(bytes[offset])
                    id += (m & 0x7f) * pow(2, 7 * i)
                    offset += 1
                    i += 1

                id += (m & 0x7f) * pow(2, 7 * i)
                offset += 1
                i += 1

                # print("解析id", m, id)

            # 解析route
            if msgHasRoute(type):
                if compressRoute:
                    route = (bytes[offset] << 8) | bytes[offset + 1]
                    offset += 2
                else:
                    routeLen = bytes[offset]
                    offset += 1
                    if routeLen:
                        route = bytearray(routeLen)
                        for i in range(routeLen):
                            route[i] = bytes[offset + i]
                        route = Protocol.strdecode(route)
                    else:
                        route = ""
                    offset += routeLen

            # 解析body
            bodyLen = bytesLen - offset
            body = bytearray(bodyLen)
            for i in range(bodyLen):
                body[i] = bytes[offset + i]

            # 返回解析后的消息对象
            return {
                "id": id,
                "type": type,
                "zip": zip,
                "compressRoute": compressRoute,
                "route": route,
                "body": body,
            }
        
Message = Protocol.Message
Package = Protocol.Package
    
# 判断消息类型是否有id
def msgHasId(type):
    return type == Message.TYPE_REQUEST or type == Message.TYPE_RESPONSE

# 判断消息类型是否有路由
def msgHasRoute(type):
    return type == Message.TYPE_REQUEST or type == Message.TYPE_NOTIFY or type == Message.TYPE_PUSH

# 计算消息id所占字节数
def caculateMsgIdBytes(id):
    len = 0
    # 循环计算id所占字节数
    while id > 0:
        len += 1
        id >>= 7
    return len

def encodeMsgFlag(type, compressRoute, buffer, offset, zip):
    if (
        type != Message.TYPE_REQUEST and
        type != Message.TYPE_NOTIFY and
        type != Message.TYPE_RESPONSE and
        type != Message.TYPE_PUSH
    ):
        raise ValueError("unknown message type: " + str(type))

    # 将压缩路由标志、消息类型和压缩标志组合成一个字节，并写入缓冲区
    buffer[offset] = ((1 if zip else 0) << 4) | (type << 1) | (1 if compressRoute else 0)
    # 返回偏移量加上消息标志字节数
    return offset + MSG_FLAG_BYTES

def encodeMsgId(id, buffer, offset):

    while id != 0:
        tmp = id % 128
        next = id // 128
        if next != 0:
            tmp += 128
        buffer[offset] = tmp
        offset += 1
        id = next
    # 返回偏移量
    return offset

def encodeMsgRoute(compressRoute, route, buffer, offset):
    # 如果启用了路由压缩
    if compressRoute:
        # 如果路由编号超出范围
        if route > MSG_ROUTE_CODE_MAX:
            raise ValueError("route number is overflow")
        # 将路由编号写入buffer
        buffer[offset] = (route >> 8) & 0xff
        buffer[offset + 1] = route & 0xff
        offset += 2
        # 如果未启用路由压缩
    else:
        # 如果路由存在
        if route:
        # 将路由长度写入buffer
            buffer[offset] = len(route) & 0xff
            # 将路由内容写入buffer
            for i in range(len(route)):
                buffer[offset + 1 + i] = ord(route[i])
                offset += len(route) + 1
            # 如果路由不存在
            else:
                buffer[offset] = 0
                offset += 1

    return offset

def encodeMsgBody(msg, buffer, offset):
    buffer[offset:offset+len(msg)] = msg
    return offset + len(msg)