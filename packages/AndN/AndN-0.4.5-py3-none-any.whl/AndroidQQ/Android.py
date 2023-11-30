import time
from typing import Union

from AndTools import pack_u
from pydantic import BaseModel

import AndroidQQ.struct.OidbSvc as OidbSvc
import AndroidQQ.struct.StatSvc as StatSvc
import AndroidQQ.pack.friendlist as friendlist
import AndroidQQ.struct.wtlogin as wt_login
from AndroidQQ.Tcp import start_client
from AndroidQQ.pack import *
from AndroidQQ.pack.MQUpdateSvc_com_qq_ti_web_scanlogin import *
from AndroidQQ.pack.SQQzoneSvc import SQQzoneSvc_shuoshuo, SQQzoneSvc_shuoshuo_rsp
from AndroidQQ.pack.SummaryCard import SummaryCard_ReqSummaryCard, SummaryCard_ReqSummaryCard_rsp

from AndroidQQ.struct import MessageSvc
from AndroidQQ.struct.Avatarlnfo import GetAvatarInfo, GetAvatarInfo_res
from AndroidQQ.struct.QQService import SvcReqGetDevLoginInfo, GetDevLoginInfo_profile, GetDevLoginInfo_res
from AndroidQQ.struct.SummaryCard import ReqSummaryCard
from AndroidQQ.struct.head import *
from AndroidQQ.struct.push import SvcReqRegister


class cookies(BaseModel):
    skey: str = None
    client_key: str = None


class device(BaseModel):
    # 软件信息
    version: str = None
    package_name: str = None  # com.tencent.qqlite
    Sig: str = None  # A6 B7 45 BF 24 A2 C2 77 52 77 16 F6 F3 6E B6 8D
    build_time: int = None  # 软件构建时间 1654570540
    sdk_version: str = None  # #6.0.0.2366
    client_type: str = None  # android
    app_id: int = None  # 似乎可以传空
    var: str = None

    # 设备信息
    name: str = 'android'
    internet: str = 'China Mobile GSM'
    internet_type: str = 'wifi'
    model: str = 'V1916A'
    brand: str = 'vivo'
    Mac_bytes: bytes = None  # '02:00:00:00:00:00'
    Bssid_bytes: bytes = None  # '00:14:bf:3a:8a:50'
    android_id: bytes = None  # 4cba299189224ca5 Android 操作系统中设备的一个唯一ID。每个设备在首次启动时都会生成一个随机的64位数字作为其
    boot_id: str = '65714910-7454-4d01-a148-6bdf337a3812'  # Linux系统中用来唯一标识系统自上次启动以来的运行时期的标识符
    Imei: str = None
    Mac: str = None  # 02:00:00:00:00:00
    Bssid: str = None  # 00:14:bf:3a:8a:50


class UN_Tlv_list(BaseModel):
    T10A_token_A4: bytes = b''
    T143_token_A2: bytes = b''
    T100_qr_code_mark: bytes = b''  # watch
    T018: bytes = b''  # watch
    T019: bytes = b''  # watch
    T065: bytes = b''  # watch
    T108: bytes = b''
    T10E: bytes = b''
    T134: bytes = b''
    T114: bytes = b''
    T133: bytes = b''
    T16A: bytes = b''
    T106: bytes = b''
    T146: Union[str, dict] = None
    T192_captcha: str = None
    T104_captcha: bytes = b''
    T546_captcha: bytes = b''


#


class info_model(BaseModel):
    uin: str = '0'
    uin_name: str = None
    password: str = None
    seq: int = 5267
    share_key: bytes = None
    key_rand: bytes = get_random_bin(16)
    key_tgtgt: bytes = None
    key_Pubkey: bytes = None  # 公钥
    Guid: bytes = get_random_bin(16)
    login_time: int = int(time.time())
    UN_Tlv_list: UN_Tlv_list = UN_Tlv_list()
    device: device = device()
    cookies: cookies = cookies()
    Tips: str = None


class AndroidQQ:
    def __init__(self, **kwargs):
        """
        :param client_type: QQ or Watch
        :param kwargs:
        """
        self.info = info_model()
        # self.info.device.Bssid_bytes = bytes.fromhex(get_md5('00:14:bf:3a:8a:50'.encode()))
        client_type = kwargs.setdefault('client_type', 'QQ')
        self.info.device.Imei = '862542082770767'
        self.info.device.Mac = '89:C2:A9:C5:FA:E9'
        self.info.device.Bssid = '00:14:bf:3a:8a:50'

        self.info.key_tgtgt = get_random_bin(16)
        self.info.key_rand = get_random_bin(16)

        self.info.device.client_type = client_type
        if client_type == 'QQ':
            self.info.device.app_id = 537170024
            self.info.device.android_id = bytes.fromhex('d018b704652f41f4')
            self.info.device.package_name = 'com.tencent.mobileqq'
            self.info.device.var = '||A8.9.71.9fd08ae5'.encode()

        elif client_type == 'QQ_old':
            """旧版本支持"""
            self.info.device.app_id = 537116186
            self.info.device.package_name = 'com.tencent.mobileqq'
            self.info.device.android_id = '4cba299189222ca6'.encode()
            self.info.device.version = '8.8.85'
            self.info.device.Sig = 'A6 B7 45 BF 24 A2 C2 77 52 77 16 F6 F3 6E B6 8D'
            self.info.device.build_time = 1645432578
            self.info.device.sdk_version = '6.0.0.2497'
            self.info.device.var = '|877408608703263|A8.8.90.83e6c009'
            # self.info.device.app_id = 537119623


        elif client_type == 'Watch':
            self.info.device.app_id = 537140974
            self.info.device.android_id = bytes.fromhex('4cba299189224ca2')
            self.info.uin = '0'
            self.info.device.package_name = 'com.tencent.qqlite'
            self.info.device.version = '2.1.7'
            self.info.device.Sig = 'A6 B7 45 BF 24 A2 C2 77 52 77 16 F6 F3 6E B6 8D'
            self.info.device.build_time = int('1654570540')  # 2022-06-07 10:55:40 软件构建时间
            self.info.device.sdk_version = '6.0.0.2366'
            self.info.key_Pubkey = bytes.fromhex(
                '04 04 6E 31 F8 59 79 DF 7F 3D F0 31 CD C6 EB D9 B9 8E E2 E2 F6 3E FB 6E 79 BC 54 BF EE FB 0F 60 24 07 DA 8C 41 4A 34 EF 46 10 A7 95 48 0E F8 3F 0E')  # 49 长度的
            self.info.share_key = bytes.fromhex('54 9F 5C 3A B4 8D B9 16 DA 96 5F 3B 1B C1 03 4B')
            self.info.key_rand = bytes.fromhex('70 3F 79 79 55 78 2E 55 63 64 3A 44 38 49 7A 53')
            self.info.Guid = bytes.fromhex('9b6be0653a356f4fac89926f3f1ceb7e')
            self.info.device.var = bytes(IMEI, 'utf-8')

        self._tcp = start_client(_func=self.UN_data)
        self.pack_list = {}

    def Set_TokenA(self, data):

        """
        appid
            537085851 小栗子二开
            537101242 小栗子

        """
        json_data = json.loads(data)
        device_APPID = json_data.get('device_APPID')

        if device_APPID is not None:
            # 向下兼容
            appid = int.from_bytes(bytes.fromhex(device_APPID), 'big')
        else:
            # 获取appid
            appid = int(json_data.get('Appid', self.info.device.app_id))

        # appid = int('537085851')
        # print('appid', appid)
        self.info.uin = str(json_data['UIN'])
        self.info.UN_Tlv_list.T10A_token_A4 = bytes.fromhex(json_data['token_A4'])
        self.info.UN_Tlv_list.T143_token_A2 = bytes.fromhex(json_data['token_A2'])
        self.info.share_key = bytes.fromhex(json_data['Sharekey'].replace(' ', ''))
        self.info.Guid = bytes.fromhex(json_data['GUID_MD5'])
        self.info.device.app_id = appid  # 现在必须验证这个参数了
        self.info.UN_Tlv_list.T10E = bytes.fromhex(json_data.get('T10E', ''))
        self.info.UN_Tlv_list.T114 = bytes.fromhex(json_data.get('T114', ''))

        self.info.UN_Tlv_list.T133 = bytes.fromhex(json_data['T133'])
        self.info.UN_Tlv_list.T134 = bytes.fromhex(json_data['T134'])

    def UN_data(self, data):
        """解包"""
        pack = pack_u(data)
        pack.get_int()
        pack_way = pack.get_byte()

        pack.get_byte()  # 00
        _len = pack.get_int()
        pack.get_bin(_len - 4)  # Uin bin
        _data = pack.get_all()
        if pack_way == 2:
            # 登录相关
            _data = TEA.decrypt(_data, '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
        elif pack_way == 1:
            _data = TEA.decrypt(_data, self.info.share_key)
        else:
            _data = b''
            log.info('未知的解密类型')

        if _data == b'':
            return
        else:
            pack = pack_u(_data)
            _len = pack.get_int()
            part1 = pack.get_bin(_len - 4)
            _len = pack.get_int()
            part2 = pack.get_bin(_len - 4)
            # part1
            pack = pack_u(part1)
            seq = pack.get_int()
            pack.get_int()
            _len = pack.get_int()
            Tips = pack.get_bin(_len - 4).decode('utf-8')
            _len = pack.get_int()
            Cmd = pack.get_bin(_len - 4).decode('utf-8')
            # print('包序号', seq, '包类型', Cmd, part2.hex())
            if Tips != '':
                seq = self.info.seq  # 推送到最后一个包
                self.info.Tips = Tips
                # log.warning(f'Tips:{Tips}')
            # part2
            # log.info('包序号', ssoseq, '包类型', Cmd, part2.hex())
            if 0 < seq < 1000000:
                # log.info('包序号', seq, '包类型', Cmd, part2.hex())
                self.pack_list.update({seq: part2})
            else:
                # log.info('推送包', seq, '包类型', Cmd, part2.hex())
                pass

    def Tcp_send(self, data):
        self._tcp.sendall(data)
        start_time = time.time()  # 获取当前时间
        seq = self.info.seq
        while time.time() - start_time < 3:  # 检查是否已过去三秒
            data = self.pack_list.get(seq)
            if data is not None:
                self.pack_list.pop(seq)  # 删除已经取出的包
                break
            time.sleep(0.1)
        self.info.seq = seq + 1

        return data

    def tcp_task(self, req_func, rsp_func):
        buffer = req_func(self.info)
        buffer = self.Tcp_send(buffer)
        if buffer == b'':
            if self.info.Tips is not None:
                message = self.info.Tips
            else:
                message = '返回空包体'

            return {'status': -99, 'message': message}
        elif buffer is None:
            return {'status': -1, 'message': '未返回数据'}
        response = rsp_func(buffer)
        return {'status': 0, 'message': '请求成功', 'response': response}

    def scan_code_auth(self, **kwargs):
        """扫码授权"""

        def req_func(info):
            return wt_login.trans_emp_auth(info, **kwargs)

        def rsp_func(buffer):
            return wt_login.trans_emp_auth_res(buffer, self.info, **kwargs)

        return self.tcp_task(req_func, rsp_func)

    def no_tail_login(self):
        """无尾登录包"""

        def req_func(info):
            return OidbSvc_0x88d_1(info, 849829771)

        return self.tcp_task(req_func, OidbSvc_0x88d_1_rep)

    def scan_Login(self, service_type: int, token: str):
        """扫码登录/辅助验证"""

        def req_func(info):
            return web_scanlogin(info, service_type, token)

        return self.tcp_task(req_func, web_scanlogin_req)

    def get_dev_login_info(self, iGetDevListType: int = 7):
        """
        获取设备登录信息
        参数:
            iGetDevListType: int, optional
                设备列表类型。如果未指定，将使用默认值 7。

        """

        def req_func(info):
            item = SvcReqGetDevLoginInfo(
                vecGuid=self.info.Guid,
                iTimeStam=1,
                strAppName='com.tencent.mobileqq',
                iRequireMax=20,
                iGetDevListType=iGetDevListType

            )
            return GetDevLoginInfo_profile(info, item)

        return self.tcp_task(req_func, GetDevLoginInfo_res)

    def get_summary_card(self, Uin: int = None, ComeFrom: int = 0):
        """"
        获取自身卡片
            参数:
            Uin: int, optional
                目标用户uin 不填获取自身
            ComeFrom: int, optional
                来源 0=自己 1=其他 31=搜索

        """

        def req_func(info):
            _ComeFrom = ComeFrom

            if Uin is None:
                _Uin = info.uin
            else:
                _Uin = Uin
                if ComeFrom == 0:
                    _ComeFrom = 1  # 其他

            Buffer = ReqSummaryCard(
                Uin=_Uin,
                ComeFrom=_ComeFrom,  # 自身是0,别人是其他 暂时不管细节
                IsFriend=True,
                GetControl=69181,
                AddFriendSource=10004,
                # stLocaleInfo=User_Locale_Info,
                SecureSig=bytes.fromhex('00'),
                ReqMedalWallInfo=True,  # 勋章墙,
                ReqNearbyGodInfo=True,  # 附近的信息
                ReqExtendCard=True,  # 请求扩展卡
                RichCardNameVer=True  # 富卡名称验证

            ).to_bytes()
            return SummaryCard_ReqSummaryCard(info, Buffer)

        return self.tcp_task(req_func, SummaryCard_ReqSummaryCard_rsp)

    def Qzone_like(self, target_Uin: int, title: str, feedskey: str):
        """
        空间点赞
        """

        def req_func(info):
            return SQQzoneSvc_like(info, target_Uin, title, feedskey)

        return self.tcp_task(req_func, SQQzoneSvc_like_rsp)

    def Qzone_shuoshuo(self, Uin, fullText: bool = False):
        """
         说说列表
            :param Uin int 说说的目标
            :param fullText bool 是否返回原始的全文信息
        """

        def req_func(info):
            return SQQzoneSvc_shuoshuo(info, Uin)

        def rsp_func(buffer):
            return SQQzoneSvc_shuoshuo_rsp(buffer, fullText)

        return self.tcp_task(req_func, rsp_func)

    def get_phone(self):
        """获取手机号"""

        def req_func(info):
            return OidbSvc_0xeb8(info)

        return self.tcp_task(req_func, OidbSvc_0xeb8_rep)

    def heartbeat(self):
        """心跳包"""

        def req_func(info):
            return Heartbeat_Alive(info)

        return self.tcp_task(req_func, Heartbeat_Alive_rsp)

    def unsubscribe(self, puin: int, cmd_type: int = 2):
        """
        取消订阅
            参数:
                puin: int 目标
                    2720152058 QQ团队
                    1770946116 安全中心
                    2290230341 QQ空间动态
                    2747277822 QQ手游
                    2010741172 QQ邮箱提醒


                cmd_type: int 默认2
        """

        def req_func(info):
            return OidbSvc_0xc96(info, puin, cmd_type)

        return self.tcp_task(req_func, OidbSvc_0xc96_rsp)

    def get_auth_list(self, start: int = 0, limit: int = 10):
        """
        获取授权列表
            参数:
                start = 0
                limit= 10
        """

        def req_func(info):
            return OidbSvc_0xc05(info, start, limit)

        return self.tcp_task(req_func, OidbSvc_0xc05_rep)

    def get_avatar_info(self, **kwargs):
        """获取头像信息"""

        def req_func(info):
            return GetAvatarInfo(info, **kwargs)

        return self.tcp_task(req_func, GetAvatarInfo_res)

    def login_register(self, lBid: int = 7, iStatus: int = 11, iOSVersion: int = 25, bOnlinePush: bool = True):
        """
        登录注册
            参数
                lBid: int
                    默认:7
                    0 登出 7 登录
                iStatus: int
                    默认:11
                    11:在线
                    21:离线
                iOSVersion: int
                    默认:25
                bOnlinePush: bool  是否在线推送
                    默认:True

        """

        def req_func(info):
            Buffer = SvcReqRegister(
                lUin=info.uin,
                lBid=lBid,
                iStatus=iStatus,
                iOSVersion=iOSVersion,
                cNetType=1,  # 网络类型
                vecGuid=info.Guid,
                strOSVer='7.1.2',  # Build.VERSION.RELEASE todo 不应该固定
                bOnlinePush=bOnlinePush,
                iLargeSeq=41,

            ).to_bytes()

            return StatSvc_register(info, Buffer)

        return self.tcp_task(req_func, StatSvc_register_rsp)

    def watch_scan_code(self, verify=False):
        """手表扫码"""
        data = wt_login.trans_emp(self.info, verify)
        data = self.Tcp_send(data)
        data = wt_login.trans_emp_res(data, self.info, verify)
        return data

    def login(self, **kwargs):
        """登录"""
        data = wt_login.login(self.info, **kwargs)
        data = self.Tcp_send(data)
        wt_login.login_res(data, self.info)

    def login_captcha(self, Ticket: str):
        """提交验证码"""
        data = wt_login.login_captcha(self.info, Ticket)
        data = self.Tcp_send(data)
        wt_login.login_res(data, self.info)

    def get_specified_info(self):
        """获取指定信息"""
        # 兼容其他源码
        data = {
            "UIN": self.info.uin,
            "GUID_MD5": self.info.Guid.hex(),
            "token_A4": self.info.UN_Tlv_list.T10A_token_A4.hex(),
            "token_A2": self.info.UN_Tlv_list.T143_token_A2.hex(),
            "Sharekey": self.info.share_key.hex(),
            "T134": self.info.UN_Tlv_list.T134.hex(),
            "T133": self.info.UN_Tlv_list.T133.hex(),
            "T10E": self.info.UN_Tlv_list.T10E.hex(),
            "T114": self.info.UN_Tlv_list.T114.hex(),
            "device_APPID": self.info.device.app_id.to_bytes(4, 'big').hex()
        }
        return json.dumps(data)

    def get_unread_msg_count(self):
        """获取未读消息"""
        data = MessageSvc.PullUnreadMsgCount(self.info)
        data = self.Tcp_send(data)
        if data:
            data = MessageSvc.PullUnreadMsgCount_res(data)
        return data

    def del_auth_info(self, **kwargs):
        """删除授权信息
        appid= 要删除的id
        """
        data = OidbSvc.P0xccd(self.info, **kwargs)
        data = self.Tcp_send(data)
        if data:
            data = OidbSvc.P0xccd_res(data)
        return data

    def del_login_info(self, **kwargs):
        """删除登录信息
        key= 获取设备信息返回
        """

        data = StatSvc.DelDevLoginInfo(self.info, **kwargs)
        data = self.Tcp_send(data)
        if data:
            data = StatSvc.DelDevLoginInfo_res(data)
        return data

    def get_friends_online_list(self, **kwargs):
        """获取在线好友列表
        'ifgetFriendVideoAbi': 是否获取朋友的视频能力。布尔值，可选，默认为False。
        'isReqCheckIn': 是否请求签到。布尔值，可选，默认为False。
        'ifShowTermType': 是否显示好友的设备类型。布尔值，可选，默认为True。
        'version': 版本号。32位整数，可选，默认为33。
        'cSrcType': 来源类型。32位整数，可选，默认为1。
        """
        data = friendlist.GetSimpleOnlineFriendInfoReq(self.info)
        data = self.Tcp_send(data)
        if data:
            data = friendlist.GetSimpleOnlineFriendInfoReq_res(data)
        return data
