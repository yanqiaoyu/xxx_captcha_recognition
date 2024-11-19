from fastapi import APIRouter, File, Form,  UploadFile
from pydantic import BaseModel
from utils.recognize import Recognize
import time
import os
import re
captchaRecogRouter = APIRouter()

# 存放验证码的路径
save_picture_path = './pic/'


class ResponseModel(BaseModel):
    data: dict
    meta: dict


'''
存储产品线及其对应的训练数据的字典
未来如果需要拓展到其他产品线,可以在这里添加
'''
product_map = {
    'ads': 'ads.traineddata',
}

# 当前只支持png格式的图片
allowed_picture_type_list = ['png']
# 最大允许上传10M
allowed_picture_size = 1024 * 1024 * 5


@captchaRecogRouter.post("/api/v2/recognize", response_model=ResponseModel)
async def PostRecogReq(
        product_name: str = Form(..., max_length=96, description="产品线名称"),
        picture: UploadFile = File(..., description="验证码图片")
):
    '''
    处理图像识别的接口
    '''

    train_data = ''
    picture_name = ''
    recognize_result = ''

    # 1. 确定产品线及其对应的训练数据
    if product_name not in product_map:
        allowed_product_name_list = []
        for key in product_map:
            allowed_product_name_list.append(key)

        result_model = ResponseModel(
            data={"status_code": 400},
            meta={
                "message": f"当前暂不支持{product_name}产品,支持的产品如下",
                "supported_product": allowed_product_name_list
            }
        )
        return result_model
    else:
        train_data = product_map[product_name]

    # 2.确定验证码图片类型及图片大小
    if picture.filename.split('.')[-1] not in allowed_picture_type_list:
        result_model = ResponseModel(
            data={"status_code": 400},
            meta={
                "message": f"当前暂不支持{picture.filename.split('.')[-1]}格式,支持的文件类型如下",
                "supported_type": allowed_picture_type_list
            }
        )
        return result_model

    # 这里只读6M,一来是为了能够触发下面的比较,二来是不想读太多影响效率
    picture_contents = await picture.read(1024*1024*6)

    if len(picture_contents) > allowed_picture_size:
        result_model = ResponseModel(
            data={"status_code": 400},
            meta={
                "message": f"验证码过大,已经超过5MB",
            }
        )
        return result_model

    # 3.保存验证码图片

    # 毫秒级的时间戳,避免出现图片名重复导致异常
    picture_name = picture.filename.split(
        '.')[0] + str(round(time.time() * 1000)) + '.png'

    try:
        with open(f"{save_picture_path}{picture_name}", 'wb') as f:
            f.write(picture_contents)
        f.close()
    except Exception as e:
        result_model = ResponseModel(
            data={"status_code": 500,
                  },
            meta={"message": "验证码图片处理失败",
                  "error": e
                  }
        )
        return result_model

    # 4.进行图像识别, 得到结果
    recognize_result = Recognize(picture_name)

    # 5.删除保存的图片
    try:
        os.remove(save_picture_path+picture_name)
    except Exception as e:
        result_model = ResponseModel(
            data={"status_code": 500,
                  },
            meta={"message": "验证码图片处理失败",
                  "error": e
                  }
        )
        return result_model

    # 6.返回结果
    if recognize_result:
        result_model = ResponseModel(
            data={"status_code": 200,
                  "result": recognize_result
                  },
            meta={"message": "识别成功",
                  "used_train_data": train_data
                  }
        )

        return result_model
    else:
        result_model = ResponseModel(
            data={"status_code": 500,
                  "result": recognize_result
                  },
            meta={"message": "识别失败",
                  "used_train_data": train_data
                  }
        )


def ocr(img) -> str:
    """
    通过带带弟弟库识别图片中的文本
    @param    img: 图片
    @return:  字符串
    """
    import ddddocr
    dddd = ddddocr.DdddOcr(show_ad=False)
    return dddd.classification(img)


def strip_verify_code(code: str) -> str:
    return re.sub(r'\W+', '', code)


@captchaRecogRouter.post("/api/v2/apex/recognize", response_model=ResponseModel)
async def PostApexRecogReq(picture: UploadFile = File(..., description="验证码图片")
):
    '''
    处理图像识别的接口，使用ddddocr库
    '''

    # 1.确定验证码图片类型及图片大小
    if picture.filename.split('.')[-1] not in allowed_picture_type_list:
        result_model = ResponseModel(
            data={"status_code": 400},
            meta={
                "message": f"当前暂不支持{picture.filename.split('.')[-1]}格式,支持的文件类型如下",
                "supported_type": allowed_picture_type_list
            }
        )
        return result_model

    # 这里只读6M,一来是为了能够触发下面的比较,二来是不想读太多影响效率
    picture_contents = await picture.read(1024*1024*6)

    if len(picture_contents) > allowed_picture_size:
        result_model = ResponseModel(
            data={"status_code": 400},
            meta={
                "message": f"验证码过大,已经超过5MB",
            }
        )
        return result_model

    # 2.保存验证码图片

    # 毫秒级的时间戳,避免出现图片名重复导致异常
    picture_name = picture.filename.split(
        '.')[0] + str(round(time.time() * 1000)) + '.png'

    try:
        with open(f"{save_picture_path}{picture_name}", 'wb') as f:
            f.write(picture_contents)
        f.close()
    except Exception as e:
        result_model = ResponseModel(
            data={"status_code": 500,
                  },
            meta={"message": "验证码图片处理失败",
                  "error": e
                  }
        )
        return result_model




    # 3. 使用ddddocr进行图像识别
    try:
        recognize_result = ocr(picture_contents)
    except Exception as e:
        result_model = ResponseModel(
            data={"status_code": 500},
            meta={"message": "验证码图片识别失败",
                  "error": str(e)
                  }
        )
        return result_model

    # 4. 返回结果
    if recognize_result:
        result_model = ResponseModel(
            data={"status_code": 200,
                  "result": strip_verify_code(recognize_result)
                  },
            meta={"message": "识别成功",
                  "used_train_data": None
                  }
        )
    else:
        result_model = ResponseModel(
            data={"status_code": 500,
                  "result": recognize_result
                  },
            meta={"message": "识别失败",
                  "used_train_data": None
                  }
        )

    return result_model