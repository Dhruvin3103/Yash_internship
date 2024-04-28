import replicate
from decouple import config


def gen_mul_six(url,replicate):
    # replicate = replicate.Client(api_token=config('REPLICATE_API_TOKEN'))
    input = {
        "image_path": url,
        "export_texmap": False,
        "export_video": False,
        "sample_steps": 75,
        "remove_background": True
    }

    output = replicate.run(
        "camenduru/instantmesh:4f151757fd04d508b84f2192a17f58d11673971f05d9cb1fd8bd8149c6fc7cbb",
        input=input
    )
    print(output[0],'multi view se aya huwa ')
    return output[0]
# print(output)
#=> ["https://replicate.delivery/pbxt/f309uxIE1MQbcCazIYuIA66...
# "https://res.cloudinary.com/dztwsdfiz/image/upload/v1714124119/tdfiznl4cxgb09u7a26u.jpg"