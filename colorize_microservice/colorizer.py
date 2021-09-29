from flask import Flask, request, send_file
import numpy as np
from flask_cors import CORS  #, cross_origin
import torchvision.transforms as transforms
from torchvision.utils import save_image
import torch
from models import Generator
from torch.autograd import Variable

import re
import base64
from io import BytesIO
from PIL import Image, ImageChops

from settings import main_opt

app = Flask(__name__)

# Cross Origin Resource Sharing (CORS) handling
CORS(app, resources={'/image': {"origins": "http://localhost:8080"}})
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

input_shape = (main_opt.channels, main_opt.img_x, main_opt.img_y)
transform = transforms.Compose(
    [
        transforms.Resize(input_shape[-2:]),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)
Tensor = torch.Tensor

# Initialize generator
generator = Generator(main_opt.latent_dim, input_shape)
generator.eval()
generator.load_state_dict(torch.load("generator_19.pth", map_location=torch.device('cpu')))

#
# @app.route("/")
# def hello():
#     return "I am OK!"


@app.route('/image', methods=['POST'])
# @cross_origin()
def image_colorize():
    # Get and format image
    data = request.json['image']
    b64_img = re.sub('^data:image/png;base64,', '', data)
    decoded_img = base64.b64decode(b64_img)
    img_ = Image.open(BytesIO(decoded_img))
    a = img_.split()[-1]
    a = ImageChops.invert(a)
    img_ = Image.merge('RGB', [a, a, a])
    input_: Tensor = transform(img_)
    real_a = input_.view(1, *input_.shape).repeat(main_opt.count_images, 1, 1, 1)
    real_a = Variable(real_a.type(Tensor))

    # Generate sampled_z
    sampled_z = Variable(Tensor(np.random.normal(0, 1, (main_opt.count_images, main_opt.latent_dim))))

    # Generate samples
    result_img = generator(real_a, sampled_z)

    result_img = torch.mean(result_img.data.cpu(), 0)
    # save_image(torch.min(input_, result_img), normalize=True)
    img_io = BytesIO()
    save_image(result_img, img_io, normalize=True, format="PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
