from Jce_b import JceWriter, JceReader

from AndroidQQ.struct.cooperation import createQmfUpstream, UnQmfDownstream
from AndroidQQ.struct import PackHead_QMF
from AndroidQQ.struct.NS_MOBILE_OPERATION import operation_like_req, operation_like_rsp


def SQQzoneSvc_like(info, target_Uin: int, title: str, feedskey: str):
    def _operation_like_req():
        int64 = JceWriter().write_int64(int(info.uin), 0).bytes()
        curkey = f'http://user.qzone.qq.com/{target_Uin}/mood/{feedskey}'

        busi_param = {
            # 最终生成的会和腾讯有所不同,但似乎没有影响
            97: f'&feedtype1=1&feedtype2=3&feedtype3=1&org_uniq_key=&sUniqId={target_Uin}_311_{feedskey}&fExposUniqId=&colorexptid=0&colorstrategyid=0',
            156: f'appid:311 typeid:0 feedtype:2 hostuin:{info.uin} feedskey:{feedskey} ',
            4: '',
            5: curkey,
            101: f'0=&1=&2=&3=&4={target_Uin}&5=&6=0&7=&8=&9=&10=0&76=',
            6: curkey,
            104: '',
            141: '',
            142: '5',
            207: '0',
            48: '0',
            52: '',
            23: '0',
            184: title,
            121: f'&feedtype1=1&feedtype2=3&feedtype3=1&org_uniq_key=&sUniqId={target_Uin}_311_{feedskey}&fExposUniqId=&colorexptid=0&colorstrategyid=0'}

        OperationLikeReq = operation_like_req(uin=int(info.uin),
                                              curkey=curkey,
                                              unikey=curkey,
                                              action=0,
                                              appid=311,
                                              busi_param=busi_param,
                                              hostuin=0
                                              ).to_bytes()

        OperationLikeReq = JceWriter().write_jce_struct(OperationLikeReq, 0)
        _Buffer = JceWriter().write_map({'like': {
            'NS_MOBILE_OPERATION.operation_like_req': OperationLikeReq
        }, 'hostuin': {'int64': int64}}, 0)
        return _Buffer

    BusiBuff = _operation_like_req()
    Upstream = createQmfUpstream(info, 1, BusiBuff, 'QzoneNewService.like')
    Buffer = PackHead_QMF(info, 'SQQzoneSvc.like', Upstream)
    return Buffer


# def SQQzoneSvc_like(info):
#     """"
#         点赞包
#     """
#
#     def createBusiControl():
#         Qmf_Busi_Control = QmfBusiControl(
#
#             # paramBoolean, paramArrayOfbyte.length, this.SUPPORT_COMPRESS ??
#             compFlag=1,
#             lenBeforeComp=860,
#             rspCompFlag=1
#         ).to_bytes()
#         _Buffer = JceWriter().write_jce_struct(Qmf_Busi_Control, 0)
#
#         _Buffer = JceWriter().write_map({'busiCompCtl': {
#             'QMF_PROTOCAL.QmfBusiControl': _Buffer
#         }}, 0)
#         return _Buffer
#
#     TokenInfo = QmfTokenInfo(
#         Type=64,
#         Key=b'',
#         ext_key={1: bytearray.fromhex('00')}
#     ).to_bytes()
#
#     ClientIpInfo = QmfClientIpInfo(
#         IpType=0,
#         ClientPort=0,
#         ClientIpv4=0,
#         ClientIpv6=bytearray.fromhex('00 00 00 00 00 00')
#     ).to_bytes()
#
#     _RetryInfo = RetryInfo(
#         Flag=1,
#         RetryCount=0,
#         PkgId=int(time.time() * 1000)
#
#     ).to_bytes()
#
#
#     jce = JceWriter()
#     jce.write_object(2286, 0)
#     jce.write_object(1000027, 1)
#     jce.write_object(226554375, 2)
#     jce.write_object('V1_AND_SQ_8.9.83_4680_YYB_D', 3)
#     jce.write_object('QzoneNewService.like', 4)
#     jce.write_object(
#         'i=8e47e13209285931450588fb100013d16b0b&imsi=8e47e13209285931450588fb100013d16b0b&mac=02:00:00:00:00:00&m=V1916A&o=9&a=28&sd=0&c64=1&sc=1&p=540*960&aid=8e47e13209285931450588fb100013d16b0b&f=vivo&mm=3946&cf=2798&cc=4&qimei=8e47e13209285931450588fb100013d16b0b&qimei36=8e47e13209285931450588fb100013d16b0b&sharpP=1&n=wifi&support_xsj_live=true&client_mod=default&qadid=&md5_android_id=&md5_mac=&client_ipv4=&aid_ticket=&taid_ticket=0101869FEA6C27834C685B0CF0ED44C4516C368A5F048AE3AA301973FA34D55425FBFF12CA010BAB2CE55BFB&muid=&muid_type=0&device_ext=%7B%22attri_info%22%3A%7B%22ua%22%3A%22Dalvik%5C%2F2.1.0+%28Linux%3B+U%3B+Android+9%3B+V1916A+Build%5C%2FPQ3B.190801.002%29%22%2C%22ua_i%22%3A%7B%22c_i%22%3A%2291.0.4472.114%22%2C%22s_i%22%3A%7B%22b_i%22%3A%22PQ3B.190801.002%22%2C%22b_m%22%3A%22V1916A%22%2C%22b_mf%22%3A%22vivo%22%2C%22b_r_o_c%22%3A%229%22%2C%22b_v_c%22%3A%22REL%22%2C%22b_v_i%22%3A%22G9650ZHU2ARC6%22%2C%22b_v_r%22%3A%229%22%2C%22jvm_v%22%3A%222.1.0%22%2C%22sw_s%22%3A%221%22%7D%7D%7D%2C%22font_size%22%3A1%2C%22harmony_sys_info%22%3A%7B%22harmony_pure_mode%22%3A-1%2C%22is_harmony_os%22%3Afalse%7D%2C%22hevc_compatibility_info%22%3A%5B%7B%22max_fps%22%3A30%2C%22max_luma_samples%22%3A%22921600%22%2C%22video_player_type%22%3A1%7D%5D%2C%22jump_ability%22%3A%5B9999%5D%2C%22module_name%22%3A%22pcad-reward%22%2C%22mqq_config_status%22%3A1%2C%22qi36%22%3A%228e47e13209285931450588fb100013d16b0b%22%2C%22qqb_external_exp_info%22%3A%7B%22exp_id%22%3A%5B%22gdt_tangram_qq_android_000006%22%2C%22gdt_tangram_qq_android_000010%22%5D%2C%22traffic_type%22%3A26%7D%2C%22targeting_ability%22%3A%7B%22support_quick_app_link%22%3Afalse%2C%22web_wx_mgame%22%3Atrue%7D%2C%22wechat_installed_info%22%3A%7B%22api_ver%22%3A%220%22%7D%7D&video_auto_play=1&sound_auto_play=0&qimei=8e47e13209285931450588fb100013d16b0b&longitude=&latitude=&coordtype=0&timezone=+8,id:Asia/Shanghai&is_teenager_mod=0&is_care_mod=0&feeds_new_style=1&feed_in_tab=0&AV1=1&hwlevel=1',
#         5)
#     jce.write_jce_struct(TokenInfo, 6)
#     jce.write_jce_struct(ClientIpInfo, 7)
#     jce.write_object(_operation_like_req(info), 8)
#
#     jce.write_object(createBusiControl(),
#                      9)
#     jce.write_object(0, 10)
#     jce.write_object(0, 11)
#     jce.write_jce_struct(_RetryInfo, 12)
#     Buffer = jce.bytes()
#     print(Buffer.hex())
#
#
#
#     pack = pack_b()
#     pack.add_int(len('SQQzoneSvc.like') + 4)
#     pack.add_bin(bytes('SQQzoneSvc.like', 'utf-8'))
#     pack.add_Hex('00 00 00 08')
#     pack.add_bin(get_random_bin(4))
#     pack.add_Hex('00 00 00 04')
#     _data_temp = pack.get_bytes()
#
#     pack.empty()
#     pack.add_int(len(_data_temp) + 4)
#     pack.add_bin(_data_temp)
#     _data_temp = pack.get_bytes()
#
#     pack.empty()
#     pack.add_bin(_data_temp)
#     pack.add_int(len(Buffer) + 4)
#     pack.add_bin(Buffer)
#     _data = pack.get_bytes()
#
#     Buffer = TEA.encrypt(_data, info.share_key)
#
#     Buffer = Pack_(info, Buffer, Types=11, encryption=1, sso_seq=info.seq)
#     return Buffer


def SQQzoneSvc_like_rsp(Buffer: bytes):
    rsp_Buffer, msg, ret = UnQmfDownstream(Buffer, 'like', 'NS_MOBILE_OPERATION.operation_like_rsp')
    if rsp_Buffer == b'':
        return {'Busi': {}, 'msg': msg, 'ret': ret}
    like_rsp = JceReader(rsp_Buffer).read_object(operation_like_rsp)
    return {'Busi': like_rsp.to_dict(), 'msg': msg, 'ret': ret}


if __name__ == '__main__':
    pass
