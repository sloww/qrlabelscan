#coding:utf-8
from .models import QrLabel, DataMaster,ScanRecord
import uuid

def run():
    name_space = uuid.NAMESPACE_DNS
    master_code = "011811061833"
    master_uuid = str(uuid.uuid5(name_space, master_code))
    title = "公司名称"
    describe = "您查询的是正品，请放心使用。有任何技术问题，可拨打 021-50687572 或加 QQ群 590646661 进行咨询！"
    tel = "021-50687572"
    img_url = "http://tslink-cc.oss-cn-hangzhou.aliyuncs.com/pub/noimage.png"
    md = DataMaster(master_uuid = master_uuid,
        master_code = master_code,
        title = title,
        describe = describe,
        tel = tel,
        img_url = img_url,
        ) 
    md.save() 
    
    
