import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd
from PIL import Image


images = {
    "Lion": np.asarray(Image.open('static/uploads/Tung.jpg'))
}


def show_images(img_name):
    'It will show image in widgets'
    print("Loading...")
    plt.title("Close this plot to open compressed image...")
    plt.imshow(images[img_name])
    plt.axis('off')
    plt.show()
    

def compress_image(img_name, k):
    print("processing...")
    global compressed_image
    img = images[img_name]
    
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    
    print("compressing...")
    ur,sr,vr = svd(r, full_matrices=False)
    ug,sg,vg = svd(g, full_matrices=False)
    ub,sb,vb = svd(b, full_matrices=False)
    rr = np.dot(ur[:,:k],np.dot(np.diag(sr[:k]), vr[:k,:]))
    rg = np.dot(ug[:,:k],np.dot(np.diag(sg[:k]), vg[:k,:]))
    rb = np.dot(ub[:,:k],np.dot(np.diag(sb[:k]), vb[:k,:]))
    
    print("arranging...")
    rimg = np.zeros(img.shape)
    rimg[:,:,0] = rr
    rimg[:,:,1] = rg
    rimg[:,:,2] = rb
    
    for ind1, row in enumerate(rimg):
        for ind2, col in enumerate(row):
            for ind3, value in enumerate(col):
                if value < 0:
                    rimg[ind1,ind2,ind3] = abs(value)
                if value > 255:
                    rimg[ind1,ind2,ind3] = 255

    compressed_image = rimg.astype(np.uint8)
    # plt.title("Image Name: "+img_name+"\n")
    # plt.imshow(compressed_image)
    # plt.axis('off')
    # plt.show()
    compressed_image = Image.fromarray(compressed_image)
    

if __name__ == "__main__":

    compress_image("Lion", 15)
    compressed_image.save("compressed_animal1.jpg")