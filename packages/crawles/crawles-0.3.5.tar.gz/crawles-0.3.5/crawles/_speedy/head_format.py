def head_format(header_data: str) -> dict:  # 请求数据格式化函数
    head_dict = {}
    for data in header_data.splitlines():  # 将文本以行进行分割
        data = data.strip()  # 去重字符串左边的空格
        if not data:  # 过滤掉空的数据
            continue

        if data.startswith(':'):  # 去重字符串的第一个冒号
            data = data.lstrip(':')

        key, value = data.split(':', maxsplit=1)

        # if 'accept-encoding' == str(key).lower():  # 过滤掉Accept-Encoding参数
        #     continue

        head_dict[key] = str(value).replace('^', '').strip()

    return head_dict


if __name__ == '__main__':
    data1 = '''
    
    
:Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Acs-Token: 1701090615907_1701090619385_SZwHbsHXzrDHomOYAi/gOWbWASj0FlrrZW7WvYBj0Zk2TRxwwXaJcGZrD5dbuiCVQ3iRYpuEbDCbVTfEMDdu+WEPp5h3j8s1pC3U0fY8xT0omNUuzRL64OQY4phvGQLdMTggGNOKHPshfD60HSS9ivQqZNQr99UzLfw8U5JeTO4td/oSfH0F+IVsWyin+558nO89X1yQIa1L2phSbcwuj2oFHDoisTIYERVhh6vhAOJ+PolV5XwmBdPyS/EUy7Wi2Lb79B2ZrGTKAy0jckhT0Mvmw1SN8moE3W03bad5RDbdB49m02QZ1mS1BeB+od3eVuI4PmjCbp5GjEWAXJoMjJIRq3VRYxOq1n6GfMeZMDHLBnS4n2UU+9AB1c5jUIhzUWl2WOmVF6+c3PLVFM3UbkqGV3zFnSgmob2GjY6sT7k7ZMnGC5DbFKeYk58tDdEv5UhnBoh+O+eiRh6Dic7Z+g==
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 151
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: APPGUIDE_10_6_6=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_10_6_9=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1700663511,1701073029,1701084801; BAIDUID_BFESS=CAD37C6B4AF49744EC7751CBE44D8928:FG=1; PSTM=1701089904; BDRCVFR[bIKc3BPCk_C]=OjjlczwSj8nXy4Grjf8mvqV; BIDUPSID=754A533E1A4F1B8ACCE56A0F70B49D17; BA_HECTOR=8100852000a1ak2h8g8k8l2n1im94jh1q; ZFY=GBXmatDttPlOSkQrqX3I7anf82:AhyHui9Jcl134sVG8:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[0-iYRofrloc]=OjjlczwSj8nXy4Grjf8mvqV; H_PS_PSSID=39633_39644_39664_39691_39694_39676_39678_39712_39731_39757_39675_39704_39794_39683_39820_39818_39835; delPer=0; PSINO=6; BCLID=10660218339446942898; BCLID_BFESS=10660218339446942898; BDSFRCVID=s9IOJexroG3O1Hvqj3kGMFceguweG7bTDYrEOwXPsp3LGJLVFdWiEG0Pts1-dEu-S2OOogKKLmOTHpKF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=s9IOJexroG3O1Hvqj3kGMFceguweG7bTDYrEOwXPsp3LGJLVFdWiEG0Pts1-dEu-S2OOogKKLmOTHpKF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRAOoC_-tDvDqTrP-trf5DCShUFsb5cAB2Q-XPoO3KOchqnCKtC5MU-IQxb-KbQf5mkf3fbgy4op8P3y0bb2DUA1y4vp0t3U2mTxoUJ2-KDVeh5Gqq-KXU4ebPRiWPr9QgbjahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHj_-D6jW3q; H_BDCLCKID_SF_BFESS=tRAOoC_-tDvDqTrP-trf5DCShUFsb5cAB2Q-XPoO3KOchqnCKtC5MU-IQxb-KbQf5mkf3fbgy4op8P3y0bb2DUA1y4vp0t3U2mTxoUJ2-KDVeh5Gqq-KXU4ebPRiWPr9QgbjahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHj_-D6jW3q; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1701090611; ab_sr=1.0.1_OTg2OTY0M2MwOWQwMGZlYzg5YTkwNDc0MGY1YjhlZDM4ZDZlZTRiYzE3ZWZiOWE3NDQwZmFiOTZmZDU3ODI0ZmViODFkNzFlNWI3NzM1YzA4OThjMmVjM2ZiODczMTBiYWY0YWMyMmVkYTI5YzE4MDc3NDE3ZTZlOTAyNDlmMWNmYWQwNWRmODY0MjBiZGY2ZDIzYmM1OTczMDFlZGQ5Mw==
Host: fanyi.baidu.com
Origin: https://fanyi.baidu.com
Pragma: no-cache
Referer: https://fanyi.baidu.com/?aldtype=16047
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
    
    
    '''
    print(head_format(data1))
