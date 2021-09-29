class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value

main_opt = AttributeDict()
main_opt.latent_dim = 8
main_opt.channels = 3
main_opt.img_x = 128
main_opt.img_y = 128
main_opt.count_images = 1