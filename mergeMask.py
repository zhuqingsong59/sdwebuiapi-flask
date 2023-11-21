import time
from PIL import Image
from flask import request
from flask_restful import Resource
from utils import base64_to_img, pil_to_base64


class MergeMask(Resource):
    def post(self):
        request_json = request.json
        maskList = request_json['mask_list']
        base_mask = Image.open(base64_to_img(maskList[0]))
        new_mask = Image.new('RGBA', base_mask.size)
        output_path = './static/outputs/' + \
            time.strftime('%Y%m%d%H%M%S', time.localtime(
                time.time())) + '_mask.png'
        for mask_file in maskList:
            mask = Image.open(base64_to_img(mask_file))
            assert mask.size == base_mask.size, "所有图片的大小需要相同"
            for x in range(mask.width):
                for y in range(mask.height):
                    r_base, g_base, b_base, a_base = base_mask.getpixel((x, y))
                    r_mask, g_mask, b_mask, a_mask = mask.getpixel((x, y))

                    # 合并逻辑在此处定义，这里我们仍然使用逻辑或
                    if a_base > 0 or a_mask > 0:
                        if a_base > 0:
                            new_mask.putpixel(
                                (x, y), (r_base, g_base, b_base, a_base))
                        else:
                            new_mask.putpixel(
                                (x, y), (r_mask, g_mask, b_mask, a_mask))
                    else:
                        new_mask.putpixel((x, y), (0, 0, 0, 0))
            base_mask = new_mask

        new_mask.save(output_path)

        print(new_mask)

        return {
            'data': 'data:image/png;base64,' + pil_to_base64(new_mask),
            'code': 0
        }
